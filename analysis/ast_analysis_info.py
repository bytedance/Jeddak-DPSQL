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

from analysis.ast_Info_visitor import AggInfoVisitor, BasicInfoVisitor, SturctInfoVisitor, SturctJoinInfoVisitor, \
    SturctCommonInfoVisitor, SQ_SturctJoinInfoVisitor
from exception.enum.analysis_errors_enum import AnalysisErrors
from exception.errors import AnalysisError
from parser.ast.type.node_type import NodeType, JoinConstraintType


# AnalysisInformation
class AnalysiInfo:
    def getName(self):
        pass

    def getVisitor(self):
        pass


# 基础元信息
class BasicMetaInfo(AnalysiInfo):
    """
        Get the basic meta info via sql anslysis

    """
    def __init__(self):
        self.database = None
        self.table = []
        self.tea_app_id = None
        self.event = None
        self._visitor = BasicInfoVisitor(self)

    def getName(self):
        return "Basic_Info"

    def getVisitor(self):
        return self._visitor


# 单个聚合函数的属性特征信息
class SingleAggInfo:
    """
        Get the aggregation node info via sql anslysis

    """
    def __init__(self):
        self.agg_feature_info = []
        self.scope_info = None
        self.inner_param_info = None
        self.outer_operate_info = None
        self.type_info = None
        self.node = None

    def append_feature(self, feature_info):
        self.agg_feature_info.extend(feature_info)


# 一个sql的所有的聚合函数信息
class AggInfo(AnalysiInfo):
    """
        Get the full aggregation info via sql anslysis

    """
    def __init__(self):
        # 存储SingleAggInfo
        self.agg_info_list = []
        self._visitor = AggInfoVisitor(self)

        # temp
        self.agg_ref_feature_info = None
        self.outer_agg_position_info = None
        self.inner_agg_position_info = None

    def getName(self):
        return "Agg_Info"

    def getVisitor(self):
        return self._visitor

    def build_new_single_agg_info(self):
        single_agg_info = SingleAggInfo()
        self.agg_info_list.append(single_agg_info)
        return single_agg_info


# 一个sql的所有结构信息
class StructInfo(AnalysiInfo):
    """
        Get the struct info via sql anslysis

    """
    def __init__(self, sq_flag=False):
        self.struct_feature_info = []
        self.struct_join_info = None
        self.struct_common_info = None
        self._visitor = SturctInfoVisitor(self)
        self._inner_register()
        if sq_flag is True:
            self._sq_register()

    def _inner_register(self):
        self.struct_join_info = StructJoinInfo(self)
        self.struct_common_info = SturctCommonInfo(self)
        self._visitor.register(self.struct_join_info)
        self._visitor.register(self.struct_common_info)

    def _sq_register(self):
        self.struct_join_info.sq_register()
        self._visitor.update_register(self.struct_join_info)

    def append_feature(self, feature_info):
        self.struct_feature_info.append(feature_info)

    def getName(self):
        return "Construct_Info"

    def getVisitor(self):
        return self._visitor


# 单个join信息
class SingleJoinInfo:
    """
        Get the join info via sql anslysis

    """
    def __init__(self):
        self.type = ""
        self.table1 = None
        self.table1_type = None
        self.table2 = None
        self.table2_type = None
        self.column1 = None
        self.column2 = None

    def set_table1(self, node):
        # multi table join, extract right table as table1
        if node.type == NodeType.SqlTableJoinSource:
            node = node.right_table

        if node.type == NodeType.SqlTableSource:
            self.table1 = node.table_expr
            self.table1_type = NodeType.SqlTableSource
        elif node.type == NodeType.SqlSubquerySource:
            self.table1 = None
            self.table1_type = NodeType.SqlSubquerySource
        else:
            raise AnalysisError(AnalysisErrors.JOIN_LEFT_ERROR.value, "unexpect join left table type")

    def set_sq_table1(self, node):
        # multi table join, extract right table as table1
        if node.type == NodeType.SqlTableJoinSource:
            node = node.right_table

        if node.table_expr.type == NodeType.Union_SQLSTATEMENT:
            self.table1 = None
            self.table1_type = NodeType.SqlSubquerySource
        elif node.table_expr.type == NodeType.Table_EXPR:
            self.table1 = node.table_expr
            self.table1_type = NodeType.SqlTableSource
        else:
            raise AnalysisError(AnalysisErrors.JOIN_LEFT_ERROR.value, "unexpect join left table type")

    def set_sq_table2(self, node):
        if node.table_expr.type == NodeType.Union_SQLSTATEMENT:
            self.table2 = None
            self.table2_type = NodeType.SqlSubquerySource
        elif node.table_expr.type == NodeType.Table_EXPR:
            self.table2 = node.table_expr
            self.table2_type = NodeType.SqlTableSource
        else:
            raise AnalysisError(AnalysisErrors.JOIN_RIGHT_ERROR.value, "unexpect join right table type")

    def set_table2(self, node):
        if node.type == NodeType.SqlTableSource:
            self.table2 = node.table_expr
            self.table2_type = NodeType.SqlTableSource
        elif node.type == NodeType.SqlSubquerySource:
            self.table2 = None
            self.table2_type = NodeType.SqlSubquerySource
        else:
            raise AnalysisError(AnalysisErrors.JOIN_RIGHT_ERROR.value, "unexpect join right table type")

    def set_column(self, join_condition):
        if join_condition.on_using == JoinConstraintType.USING:
            self.column1 = join_condition.conditions[0]
            self.column2 = join_condition.conditions[0]
        elif join_condition.on_using == JoinConstraintType.ON:
            self.column1 = join_condition.conditions[0].left
            self.column2 = join_condition.conditions[0].right
        else:
            raise AnalysisError(AnalysisErrors.JOIN_CONDITION_ERROR.value, "unexpect join condition type")


# 单个sql的所有join信息
class StructJoinInfo(AnalysiInfo):
    """
        Get the full join info in sql via sql anslysis

    """
    def __init__(self, struct_info):
        self._visitor = SturctJoinInfoVisitor(self)
        self.struct_info = struct_info
        self.join_feature_info = []
        self.join_infos = []

    def sq_register(self):
        self._visitor = SQ_SturctJoinInfoVisitor(self)

    def getName(self):
        return "Construct_Join_Info"

    def getVisitor(self):
        return self._visitor

    def append_join_feature(self, feature_info):
        self.join_feature_info.append(feature_info)
        self.struct_info.append_feature(feature_info)

    def get_new_join_info(self):
        join_info = SingleJoinInfo()
        self.join_infos.append(join_info)
        return join_info


# 单个sql的所有普通结构信息
class SturctCommonInfo(AnalysiInfo):
    """
        Get the full common struct info in sql via sql anslysis

    """
    def __init__(self, struct_info):
        self._visitor = SturctCommonInfoVisitor(self)
        self.struct_info = struct_info
        self.consturct_feature_info = []
        self.with_node_info = []
        self.group_node_info = []

    def add_with_node(self, node):
        self.with_node_info.append(node)

    def add_group_node(self, node):
        self.group_node_info.append(node)

    def add_feature_info(self, info):
        self.consturct_feature_info.append(info)
        self.struct_info.append_feature(info)

    def getName(self):
        return "Construct_Common_Info"

    def getVisitor(self):
        return self._visitor


# class RuleCheckInfo(AnalysiInfo):
#     def __init__(self):
#         self.strong_rules = []
#         self.weak_rules = []
#         self.all_rules = []
#         self._visitor = None
#
#     def getName(self):
#         return "Rule_Info"
#
#     def getVisitor(self):
#         return self._visitor


# class AggFuncInfo(AnalysiInfo):
#     def __init__(self):
#         self.all_info = []
#         self._visitor = None
#
#     def getName(self):
#         return "Agg_Info"
#
#     def getVisitor(self):
#         return self._visitor
