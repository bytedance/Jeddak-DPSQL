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

from analysis.syntax_feature import SqlAllFeature, AggScopeFeature, AggInnerParamFeature, AggOuterOperationFeature
from parser.ast.type.node_type import NodeType


# Structured calculation of different features, flag value True means hit
class SyntaxRuleInfo:
    def __init__(self, struct_info, agg_info):
        self.struct_info = struct_info
        self.agg_info = agg_info

    # Whether the with structure exists
    def getSturctWithRuleFlag(self):
        features = self.struct_info.struct_feature_info
        if SqlAllFeature.WITH_BLOCK in features:
            return True
        else:
            return False

    # internal parameter reference
    def getInnerAggRefFlag(self):
        if self.agg_info.outer_agg_position_info == AggScopeFeature.SCOPE_NO_OUTER and self.agg_info.agg_ref_feature_info == AggInnerParamFeature.AGG_REF:
            return True
        else:
            return False

    # The outermost aggregate function wraps the function
    def getOuterAggFuncFlag(self):
        for item in self.agg_info.agg_info_list:
            if AggOuterOperationFeature.FUNC_ALL in item.agg_feature_info and item.scope_info == AggScopeFeature.SCOPE_OUTER:
                return True

        return False

    # When there is an external aggregate function, whether the join operation contains subqueries or nested queries
    # todo：I'll disassemble it later
    def getInnerJoinFlag(self):
        if self.agg_info.outer_agg_position_info == AggScopeFeature.SCOPE_NO_OUTER:
            return False

        features = self.struct_info.struct_feature_info
        if SqlAllFeature.JOIN_OPERATOR_CONTAIN_SUBQUERY in features or SqlAllFeature.JOIN_NESTED_JOIN in features:
            return True
        else:
            return False

    # If there is an external aggregate function and the join operation is table, whether the external aggregate function is an operation other than sum and count
    # todo：I'll disassemble it later
    def getOuterJoinOperatorFlag(self):
        features = self.struct_info.struct_feature_info
        if SqlAllFeature.JOIN_OPERATOR_CONTAIN_SUBQUERY in features or SqlAllFeature.JOIN_OPERATOR_ALL_TABLE not in features:
            return False

        for item in self.agg_info.agg_info_list:
            if item.type_info != NodeType.SqlSumFunction_EXPR and item.type_info != NodeType.SqlCountFunction_EXPR:
                return True

        return False

    # Whether to include aggregate functions
    def getAggExistFlag(self):
        if len(self.agg_info.agg_info_list) == 0:
            return True

        return False

    def getOuterAggFlag(self):
        for item in self.agg_info.agg_info_list:
            if item.scope_info == AggScopeFeature.SCOPE_OUTER:
                return True

        return False

    def getInnerAggFlag(self):
        for item in self.agg_info.agg_info_list:
            if item.scope_info == AggScopeFeature.SCOPE_INNER:
                return True

        return False
