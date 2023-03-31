# Copyright (2023) Beijing Volcano Engine Technology Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from enum import Enum
from exception.errors import AnalysisError
from parser.utils import ast_utils
from parser.ast.type.node_type import NodeType
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor
from utils.singleton import Singleton


analysis_dir = os.path.dirname(__file__)


class RuleAction(Enum):
    """
        Define error action via rule verify.(To be perfected)

    """
    # throwsAnError
    Action_Throw_Error = 90001
    # print information
    Action_Print_Info = 90002
    # Continue execution without blocking
    Action_Continue = 90003


class RuleBlockFeature(Enum):
    """
        Define feature rule for block level.(To be perfected)

    """
    # The characteristics of the overall layer
    # Contains the with block
    BlockFeature_Contain_With = 1001
    # does not contain a with block
    BlockFeature_No_With = 1002
    # include select block
    BlockFeature_Contain_Select = 1003
    # does not contain select block
    BlockFeature_No_Select = 1004
    # contains the from block
    BlockFeature_Contain_From = 1005
    # does not contain the from block
    BlockFeature_No_From = 1006
    # contains where block
    BlockFeature_Contain_Where = 1007
    # does not contain where block
    BlockFeature_No_Where = 1008
    # contains the group by block
    BlockFeature_Contain_GroupBy = 1009
    # does not contain a groupby block
    BlockFeature_No_GroupBy = 1010
    # contains the having block
    BlockFeature_Contain_Having = 1011
    # does not contain the having block
    BlockFeature_No_Having = 1012
    # contains the order by block
    BlockFeature_Contain_OrderBy = 1013
    # does not contain order by block
    BlockFeature_No_OrderBy = 1014

    # The specific block location characteristics of the layer to which it belongs
    # on the with block
    BlockFeature_In_With = 1201
    # on the select block
    BlockFeature_In_Select = 1202
    # on the from block
    BlockFeature_In_From = 1203
    # on where block
    BlockFeature_In_Where = 1204
    # on the group by block
    BlockFeature_In_GroupBy = 1205
    # on the having block
    BlockFeature_In_Having = 1206
    # on the order by block
    BlockFeature_In_OrderBy = 1207


class RuleScope(Enum):
    """
        Define rule scope code.

    """
    # outermost layer or layer 1
    Scope_1 = 2001
    # second outer layer or layer 2
    Scope_2 = 2002
    # secondary outer layer or layer 3
    Scope_3 = 2003
    # layer4
    Scope_4 = 2004
    # layer5
    Scope_5 = 2005
    # innermost layer
    Scope_6 = 2006
    # sub inner layer
    Scope_7 = 2007
    # Secondary inner layer
    Scope_8 = 2008

    # all layers
    Scope_all = 2101
    # Inner layer (other layers after removing the outermost layer)
    Scope_inner = 2102

    # layer outside the current layer
    Scope_current_outer = 2201
    # layer inside the current layer
    Scope_current_inner = 2202


class RuleItem(Enum):
    """
        Define rule for item code.

    """
    # aggregation function value 3001-3099
    # sum function
    Func_Sum = 3001
    # count function
    Func_Count = 3002
    # averaging function
    Func_Avg = 3003
    # maximum function
    Func_Max = 3004
    # minimum function
    Func_Min = 3005
    # variance function
    Func_VarPop = 3006
    # square difference function
    Func_StddevPop = 3007
    # any aggregate function
    Func_AnyAgg = 3098
    # no aggregate functions
    Func_NoAgg = 3099

    # '*' select
    Item_All = 3101


@Singleton
class RuleAnalysisCenter:
    """
        Schedule center for rule verify.

        Attributes:
            default_path: The path of rule list

    """
    def __init__(self, default_path="rules"):
        full_rule_dir = os.path.join(analysis_dir, default_path)
        self.rule_dir = full_rule_dir
        self.suffix = ".json"
        self.rule_engines = None
        self.load_rules()

    # Temporarily ignore the issue of file conflicts with different rules
    # In the future, consider adding a timer here to update the new rules regularly
    def load_rules(self):
        engines = []
        for file_name in os.listdir(self.rule_dir):
            if file_name.endswith(self.suffix):
                engine = self._load_rule(file_name)
                engines.append(engine)
        self.rule_engines = engines

        # Reserve a return, on the one hand for testing, on the other hand for future expansion
        return engines

    def _load_rule(self, file_name):
        file_path = os.path.join(self.rule_dir, file_name)
        fr = open(file_path)
        # rule_content = fr.readlines()
        rule_json = json.load(fr)
        engine = self._load_engine(rule_json)
        return engine

    def _load_engine(self, rule_json):
        engine = RuleEngine()
        # The following three must exist in the rule file
        engine.action_info = rule_json.get("action")
        engine.msg = rule_json.get("msg")
        engine.rule_code = rule_json.get("rule_code")

        if "struct_info" in rule_json:
            engine.struct_info = rule_json.get("struct_info")

        if "agg_info" in rule_json:
            engine.agg_info = rule_json.get("agg_info")

        if "depend_info" in rule_json:
            engine.depend_info = rule_json.get("depend_info")

        if "influence_info" in rule_json:
            engine.influence_info = rule_json.get("influence_info")

        return engine

    def get_rule_engines(self):
        return self.rule_engines


class RuleEngine:
    """
        Define rule engine to match rule list.

    """
    def __init__(self):
        # Rule code, globally unique identifier
        self.rule_code = None

        # The feature information corresponding to the rule
        self.struct_info = None
        self.agg_info = None
        self.depend_info = None
        self.influence_info = None

        # Actions when the rule fires
        self.action_info = None
        # Prompt message after the rule is triggered
        self.msg = None

    # Engine execution: first check whether it is triggered, if it is triggered, determine the follow-up action according to the action in the rule
    def excute(self, ast):
        detect_flag = self._detect(ast)
        if detect_flag is False:
            return

        if self.action_info == RuleAction.Action_Throw_Error.value:
            raise AnalysisError("6101", self.msg)

    # Check if the input AST triggers this rule engine
    # Not perfect, need to insert rule information into the original analyzer
    # Currently only customized body for security policy
    def _detect(self, ast):
        if self.struct_info is None:
            return False
        scope = self.struct_info[0].get("scope")
        block_info = self.struct_info[0].get("blocks")
        feature_info = self.struct_info[0].get("features")

        checker = SecurityCheckVisitor(scope, block_info, feature_info)
        ast.accept(checker)

        if checker.contain_agg is False:
            # Trigger this rule on behalf of the AST
            return True
        else:
            return False


class SecurityCheckVisitor(BaseAstVisitor):
    """
        Define visitor to traverse nodes and match rules.
        Temporary plan: Feature detection and evaluation mixed together. Subsequent changes to detect features first, then evaluate features

    """
    def __init__(self, scope, block_info, feature_info):
        self.filter_scope = scope
        self.filter_blocks = block_info
        self.filter_features = feature_info

        self.contain_agg = False

    def visitSelectBlockStatement(self, node):
        if self.contain_agg is True:
            return
        agg_nodes = ast_utils.findNodes(node, NodeType.SqlAggFunction_EXPR)
        if len(agg_nodes) > 0:
            self.contain_agg = True
