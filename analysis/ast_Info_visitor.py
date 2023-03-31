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
from analysis.syntax_feature import SqlAllFeature
from parser.utils import ast_utils
from parser.ast.type.node_type import NodeType
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor


class SturctInfoVisitor(BaseAstVisitor):
    """
        Visitor for traverse structure information

    """

    def __init__(self, construct_info):
        self.construct_info = construct_info
        self.visitors = {}

    def register(self, analysis_info):
        name = analysis_info.getName()
        if name in self.visitors.keys():
            logging.warning("%s has been registered" % name)
        else:
            self.visitors[name] = analysis_info.getVisitor()

    def update_register(self, analysis_info):
        name = analysis_info.getName()
        if name in self.visitors.keys():
            self.visitors[name] = analysis_info.getVisitor()

    def visitWithBlockStatement(self, node):
        for key in self.visitors.values():
            key.visitWithBlockStatement(node)

    def visitGroupByBlockStatement(self, node):
        for key in self.visitors.values():
            key.visitGroupByBlockStatement(node)

    def visitSqlTableJoinSource(self, node):
        for key in self.visitors.values():
            key.visitSqlTableJoinSource(node)


class SturctCommonInfoVisitor(BaseAstVisitor):
    """
        A visitor that traverses common structural information needs to be registered in SturctInfoVisitor

    """

    def __init__(self, construct_common_info):
        self.consturct_common_info = construct_common_info

    def visitWithBlockStatement(self, node):
        self.consturct_common_info.add_feature_info(SqlAllFeature.WITH_BLOCK)
        self.consturct_common_info.add_with_node(node)

    def visitGroupByBlockStatement(self, node):
        self.consturct_common_info.add_feature_info(SqlAllFeature.GROUP_BY_BLOCK)
        self.consturct_common_info.add_group_node(node)


class SQ_SturctJoinInfoVisitor(BaseAstVisitor):
    """
        A visitor SQ-based that traverses join structural information.

    """

    def __init__(self, construct_join_info):
        self.consturct_join_info = construct_join_info

    def visitSqlTableJoinSource(self, node):
        left_table = node.left_table
        right_table = node.right_table
        ji = self.consturct_join_info.get_new_join_info()
        ji.type = str(node.join_type).strip()
        ji.set_sq_table1(left_table)
        ji.set_sq_table2(right_table)
        # for cross join, has no conditions
        if node.join_condition is not None:
            ji.set_column(node.join_condition)

        if self._check_inner_subquery(left_table) or self._check_inner_subquery(right_table):
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_OPERATOR_CONTAIN_SUBQUERY)
        elif left_table.type == NodeType.SqlTableSource and right_table.type == NodeType.SqlTableSource:
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_OPERATOR_ALL_TABLE)
        else:
            pass

    def _check_inner_subquery(self, node):
        nodes = ast_utils.findNodes(node, NodeType.Union_SQLSTATEMENT)
        if len(nodes) > 0:
            return True
        else:
            return False


class SturctJoinInfoVisitor(BaseAstVisitor):
    """
        The visitor that traverses the join structure information needs to be registered in SturctInfoVisitor.

    """

    def __init__(self, construct_join_info):
        self.consturct_join_info = construct_join_info

    def visitSqlTableJoinSource(self, node):
        left_table = node.left_table
        right_table = node.right_table

        ji = self.consturct_join_info.get_new_join_info()
        ji.type = str(node.join_type).strip()

        ji.set_table1(node.left_table)
        ji.set_table2(node.right_table)
        # for cross join, has no conditions
        if node.join_condition is not None:
            ji.set_column(node.join_condition)

        if self._check_inner_subquery(left_table) or self._check_inner_subquery(right_table):
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_OPERATOR_CONTAIN_SUBQUERY)
        elif left_table.type == NodeType.SqlTableSource and right_table.type == NodeType.SqlTableSource:
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_OPERATOR_ALL_TABLE)
        else:
            pass

        if self._check_nested_join(right_table):
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_NESTED_JOIN)

        # todo: There may be omissions
        if left_table.type != NodeType.SqlTableJoinSource and self._check_nested_join(left_table):
            self.consturct_join_info.append_join_feature(SqlAllFeature.JOIN_NESTED_JOIN)

    def _check_inner_subquery(self, node):
        nodes = ast_utils.findNodes(node, NodeType.Union_SQLSTATEMENT)
        if len(nodes) > 0:
            return True
        else:
            return False

    def _check_nested_join(self, node):
        nodes = ast_utils.findNodes(node, NodeType.SqlTableJoinSource)
        if len(nodes) > 0:
            return True
        else:
            return False


class AggInfoVisitor(BaseAstVisitor):
    """
        Visitor for traversing aggregate function information.

    """
    def __init__(self, agg_info):
        self.agg_info = agg_info

    def _filter(self, node):
        block_node = ast_utils.getCurrentBlockStatement(node)
        if block_node.type != NodeType.Select_BLOCKSTATEMENT:
            return True

    def visitSqlCountFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlCountFunction_EXPR
        current_agg_info.node = node

    def visitSqlSumFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlSumFunction_EXPR
        current_agg_info.node = node

    def visitSqlAvgFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlAvgFunction_EXPR
        current_agg_info.node = node

    def visitSqlMinFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlMinFunction_EXPR
        current_agg_info.node = node

    def visitSqlMaxFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlMaxFunction_EXPR
        current_agg_info.node = node

    def visitSqlVarPopFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlVarPopFunction_EXPR
        current_agg_info.node = node

    def visitSqlStdPopFunction(self, node):
        if self._filter(node):
            return
        current_agg_info = self.agg_info.build_new_single_agg_info()
        current_agg_info.type_info = NodeType.SqlStdPopFunction_EXPR
        current_agg_info.node = node


class BasicInfoVisitor(BaseAstVisitor):
    """
        Visitor for traversing basic meta information.

    """
    def __init__(self, basic_info):
        self.basic_info = basic_info

    def visitTable(self, node):
        if node.database is not None:
            self.basic_info.database = str(node.database).strip("`")
        self.basic_info.table.append(str(node.table).strip("`"))

    def visitBinaryEqual(self, node):
        if str(node.left).lower() == "tea_app_id":
            self.basic_info.tea_app_id = str(node.right)
        if str(node.left).lower() == "event":
            self.basic_info.event = str(node.right)


class AstInfoVisitor(BaseAstVisitor):
    """
        Root visitor for AST parsing information traversal.

    """
    def __init__(self):
        # self.basic_info_visitor = BasicInfoVisitor()
        self.visitors = {}

    def register(self, analysis_info):
        name = analysis_info.getName()
        if name in self.visitors.keys():
            logging.warning("%s has been registered" % name)
        else:
            self.visitors[name] = analysis_info.getVisitor()

    def visitTable(self, node):
        for key in self.visitors.values():
            key.visitTable(node)

    def visitBinaryEqual(self, node):
        for key in self.visitors.values():
            key.visitBinaryEqual(node)

    def visitSelectItem(self, node):
        for key in self.visitors.values():
            key.visitSelectItem(node)

    def visitSqlCountFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlCountFunction(node)

    def visitSqlSumFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlSumFunction(node)

    def visitSqlAvgFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlAvgFunction(node)

    def visitSqlMinFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlMinFunction(node)

    def visitSqlMaxFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlMaxFunction(node)

    def visitSqlVarPopFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlVarPopFunction(node)

    def visitSqlStdPopFunction(self, node):
        for key in self.visitors.values():
            key.visitSqlStdPopFunction(node)

    def visitWithBlockStatement(self, node):
        for key in self.visitors.values():
            key.visitWithBlockStatement(node)

    def visitGroupByBlockStatement(self, node):
        for key in self.visitors.values():
            key.visitGroupByBlockStatement(node)

    def visitSqlTableJoinSource(self, node):
        for key in self.visitors.values():
            key.visitSqlTableJoinSource(node)
