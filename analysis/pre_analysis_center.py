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

import logging
from enum import Enum
from analysis.ast_analysis_info import BasicMetaInfo, AggInfo, StructInfo
from analysis.ast_Info_visitor import AstInfoVisitor
from analysis.syntax_feature import AggOuterOperationFeature, AggInnerParamFeature, AggScopeFeature
from analysis.syntax_rule import SyntaxRuleInfo
from exception.enum.analysis_errors_enum import AnalysisErrors
from exception.errors import AnalysisError
from parser.ast.type.node_type import NodeType
from analysis.feature_analysis_visitor import FeatureAnalysisCenter


# noisy routing
class NoiseSwitch(Enum):
    """
         Choose the method to add noise.

    """
    # no noise
    NOT_NOISE = 40001
    # post processing noise
    NOISE_POST_PROCESS = 40002
    # overwrite noise
    NOISE_REWRITE_PROCESS = 40003


class AnalysisConfig(Enum):
    META_INFO = 0x0001
    AGG_INFO = 0x0002
    STRUCT_INFO = 0x0004
    SWITCH_INFO = 0x0008
    META_STRUCT_INFO = 0x0005

    def is_meta_set(self):
        value = self.value & 0x0001
        return value

    def is_agg_set(self):
        value = self.value & 0x0002
        return value

    def is_struct_set(self):
        value = self.value & 0x0004
        return value

    def is_switch_set(self):
        value = self.value & 0x0008
        return value


class AnalysisType(Enum):
    AST_TYPE = 90001
    SQL_TYPE = 90003


# Analysis information corresponding to a single sql
class SingleAnalysis:
    def __init__(self, src_input, input_type=AnalysisType.AST_TYPE, analysis_config=None):
        self.analysis_config = analysis_config

        # Basic database table meta information
        self.basic_meta_info = None
        # Attribute feature information related to aggregate functions
        self.agg_info = None
        # Feature information related to the overall structure of the SQL
        self.struct_info = None

        # self.join_info = None
        # self.rule_info = None
        self.noise_switch_info = None
        self.agg_info = None

        self.post_agg_list = []
        self.rewrite_agg_list = []

        if input_type == AnalysisType.AST_TYPE:
            self.sql_ast = src_input
            self._analysis_ast()
        else:
            logging.warning("not support analysis type : %s" % str(input_type.name))

    # Use the registration method for analysis. When you need to analyze new functions, you can write a new visitor and register it.
    def _analysis_ast(self):
        aav = AstInfoVisitor()

        # register all ast traversal analysis task
        # register basic meta info analysis task
        if self.analysis_config is None or self.analysis_config.is_meta_set():
            self.basic_meta_info = BasicMetaInfo()
            aav.register(self.basic_meta_info)

        # register all agg info analysis task
        if self.analysis_config is None or self.analysis_config.is_agg_set():
            self.agg_info = AggInfo()
            aav.register(self.agg_info)

        # register construct analysis task
        if self.analysis_config is None or self.analysis_config.is_struct_set():
            self.struct_info = StructInfo()
            aav.register(self.struct_info)

        self.sql_ast.accept(aav)

        # analysis agg link info
        if self.analysis_config is None or self.analysis_config.is_agg_set():
            self._analysis_agg_info()

        # analysis switch info
        if self.analysis_config is None or self.analysis_config.is_switch_set():
            self._analysis_switch_info()

    def getBasicMetaInfo(self):
        return self.basic_meta_info

    def getAggInfo(self):
        return self.agg_info

    def _analysis_agg_info(self):
        for item in self.agg_info.agg_info_list:
            feature = self._analysis_agg_outer_operation_info(item.node)
            item.append_feature(feature)

        # anaysis ref info , temp solution
        analysis_center = FeatureAnalysisCenter(self.sql_ast)
        analysis_center.analysis_basic_feature()
        args_link_result = analysis_center.get_agg_args_link_agg()
        if len(args_link_result) > 0:
            self.agg_info.agg_ref_feature_info = AggInnerParamFeature.AGG_REF

        # analysis agg position info, temp solution
        all_agg_nodes_result_1 = analysis_center.get_all_agg_nodes(analysis_center.root_scope_query, [1])
        all_agg_nodes_result_2 = analysis_center.get_all_agg_nodes_for_current_query(analysis_center.root_scope_query)

        if len(all_agg_nodes_result_2) == 0:
            self.agg_info.outer_agg_position_info = AggScopeFeature.SCOPE_NO_OUTER

        if len(all_agg_nodes_result_1) == 0:
            self.agg_info.inner_agg_position_info = AggScopeFeature.SCOPE_NO_INNER

        for node in all_agg_nodes_result_2:
            for item in self.agg_info.agg_info_list:
                if item.node == node:
                    item.scope_info = AggScopeFeature.SCOPE_OUTER

        for item in self.agg_info.agg_info_list:
            if item.scope_info is None:
                item.scope_info = AggScopeFeature.SCOPE_INNER

    def _analysis_switch_info(self):
        syntax_rule = SyntaxRuleInfo(self.struct_info, self.agg_info)

        struct_with_flag = syntax_rule.getSturctWithRuleFlag()
        if struct_with_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        inner_agg_ref_flag = syntax_rule.getInnerAggRefFlag()
        if inner_agg_ref_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        outer_func_flag = syntax_rule.getOuterAggFuncFlag()
        if outer_func_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        inner_join_flag = syntax_rule.getInnerJoinFlag()
        if inner_join_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        outer_join_operator_flag = syntax_rule.getOuterJoinOperatorFlag()
        if outer_join_operator_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        agg_exist_flag = syntax_rule.getAggExistFlag()
        if agg_exist_flag is True:
            self.noise_switch_info = NoiseSwitch.NOT_NOISE
            return

        outer_agg_flag = syntax_rule.getOuterAggFlag()
        if outer_agg_flag is True:
            self.noise_switch_info = NoiseSwitch.NOISE_POST_PROCESS
            return

        inner_agg_flag = syntax_rule.getInnerAggFlag()
        if inner_agg_flag is True:
            self.noise_switch_info = NoiseSwitch.NOISE_REWRITE_PROCESS
            return

        raise AnalysisError(AnalysisErrors.NOISE_SWITCH_ERROR.value, "Cannot choose noise switch")

    def _analysis_agg_outer_operation_info(self, agg):
        # select_item = AstUtils.getCurrentSelectItem(agg)
        feature_info = []
        if agg.type == NodeType.SelectItem_EXPR:
            pass
        elif NodeType.Function_EXPR.value <= agg.type.value < NodeType.BooleanCompare_EXPR.value:
            feature_info.append(AggOuterOperationFeature.FUNC_ALL)
            feature_info.extend(self._analysis_agg_outer_operation_info(agg.parent))
        else:
            feature_info.extend(self._analysis_agg_outer_operation_info(agg.parent))

        return feature_info

    def getStructInfo(self):
        return self.struct_info

    def getNoiseSwitchInfo(self):
        return self.noise_switch_info


# Pre-analysis center, save the pre-analysis results corresponding to all sql
class PreAnalysisCenter:
    def __init__(self):
        self.analysis_dict = {}
        self.analysis_config = None

    # Get the meta information of sql, currently you can get database, table, tea appid, event in sql
    def getBasicMetaInfo(self, sql_ast):
        single_analysis = self._get_ast_analysis_object(sql_ast)
        return single_analysis.getBasicMetaInfo()

    # Obtain aggregate function information in sql, including internal parameter information, external operation information, hierarchical information, ast nodes, etc. of the aggregate function
    def getAggInfo(self, sql_ast):
        single_analysis = self._get_ast_analysis_object(sql_ast)
        return single_analysis.getAggInfo()

    # Obtain structural information in sql, such as with structure and join structure
    def getStructInfo(self, sql_ast):
        single_analysis = self._get_ast_analysis_object(sql_ast)
        return single_analysis.getStructInfo()

    # Obtain the characteristic information of the sql hit, which is not enabled for the time being
    def getSyntaxRuleFeatures(self, sql_ast):
        single_analysis = self._get_ast_analysis_object(sql_ast)
        return single_analysis.getRuleInfo()

    # Get the noise-added routing information hit by the current sql, there are three types of routing information:
    # No noise (Noise Switch.NOT NOISE),
    # Post-processing noise (Noise Switch.NOISE REWRITE PROCESS),
    # Noise Switch.NOISE REWRITE PROCESS
    def getNoiseSwitch(self, switch_input, input_type=AnalysisType.AST_TYPE):
        if input_type == AnalysisType.AST_TYPE:
            single_analysis = self._get_ast_analysis_object(switch_input)
            return single_analysis.getNoiseSwitchInfo()
        elif input_type == AnalysisType.SQLIST_TYPE:
            single_analysis = self._get_sqlist_analysis_object(switch_input)
            return single_analysis.getNoiseSwitchInfo()
        else:
            raise AnalysisError(AnalysisErrors.NOISE_SWITCH_ERROR.value, "Unknown AnalysisType")

    def _get_ast_analysis_object(self, sql_ast):
        if sql_ast in self.analysis_dict.keys():
            single_analysis = self.analysis_dict.get(sql_ast)
        else:
            single_analysis = SingleAnalysis(sql_ast, input_type=AnalysisType.AST_TYPE,
                                             analysis_config=self.analysis_config)

        return single_analysis
