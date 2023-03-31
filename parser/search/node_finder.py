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
# Internal logic of AST operations

import logging

from parser.ast.type.node_type import NodeType


def findVisitorNodes(type, visitor):
    if type == NodeType.SqlAggFunction_EXPR:
        return visitor.all_agg_nodes
    elif type == NodeType.SqlCountFunction_EXPR:
        return visitor.count_nodes
    elif type == NodeType.SqlMinFunction_EXPR:
        return visitor.min_nodes
    elif type == NodeType.SqlMaxFunction_EXPR:
        return visitor.max_nodes
    elif type == NodeType.SqlSumFunction_EXPR:
        return visitor.sum_nodes
    elif type == NodeType.SqlAvgFunction_EXPR:
        return visitor.avg_nodes
    elif type == NodeType.SqlVarPopFunction_EXPR:
        return visitor.var_pop_nodes
    # elif type == NodeType.SqlVarSampFunction_EXPR:
    #     return visitor.var_samp_nodes
    elif type == NodeType.SqlStdPopFunction_EXPR:
        return visitor.std_pop_nodes
    # elif type == NodeType.SqlStdSampFunction_EXPR:
    #     return visitor.std_samp_nodes

    elif type == NodeType.BooleanCompare_EXPR:
        return visitor.all_nodes
    elif type == NodeType.BinaryEqual_EXPR:
        return visitor.binary_equal_nodes
    elif type == NodeType.LogicalEqual_EXPR:
        return visitor.logical_equal_nodes
    elif type == NodeType.LogicalNot_EXPR:
        return visitor.logical_not_nodes
    elif type == NodeType.LogicalAnd_EXPR:
        return visitor.logical_and_nodes
    elif type == NodeType.LogicalOr_EXPR:
        return visitor.logical_or_nodes
    elif type == NodeType.LogicalConcat_EXPR:
        return visitor.logical_concat_nodes
    elif type == NodeType.LogicalIsNull_EXPR:
        return visitor.logical_is_null_nodes
    elif type == NodeType.LogicalCompare_EXPR:
        return visitor.logical_compare_nodes
    elif type == NodeType.LogicalIn_EXPR:
        return visitor.logical_in_nodes
    elif type == NodeType.LogicalLike_EXPR:
        return visitor.logical_like_nodes
    # elif type == NodeType.LogicalBetween_EXPR:
    #     return visitor.logical_between_nodes

    elif type == NodeType.IfExpression_EXPR:
        return visitor.if_nodes
    elif type == NodeType.IIFFunction_EXPR:
        return visitor.iif_nodes
    elif type == NodeType.MultiIfExpression_EXPR:
        return visitor.multiif_nodes
    elif type == NodeType.CaseExpression_EXPR:
        return visitor.case_nodes
    elif type == NodeType.WhenExpression_EXPR:
        return visitor.when_nodes
    elif type == NodeType.TernaryExpression_EXPR:
        return visitor.ternary_nodes
    elif type == NodeType.CondExpression_EXPR:
        return visitor.all_nodes

    elif type == NodeType.Function_EXPR:
        return visitor.all_func_nodes
    elif type == NodeType.MathFunction_EXPR:
        return visitor.math_func_nodes
    elif type == NodeType.CommonFunction_EXPR:
        return visitor.common_func_nodes

    elif type == NodeType.SqlTableSource:
        return visitor.table_source_nodes
    elif type == NodeType.SqlTableJoinSource:
        return visitor.table_join_source_nodes
    # elif type == NodeType.SqlUnionSource:
    #     return visitor.table_union_source_nodes
    elif type == NodeType.SqlSubquerySource:
        return visitor.subquery_source_nodes
    # elif type == NodeType.SqlArrayJoinSource:
    #     return visitor.array_join_source_nodes
    elif type == NodeType.SqlFusionMergeSource:
        return visitor.fusion_merge_source_nodes
    elif type == NodeType.SqlSource:
        return visitor.all_source_nodes

    elif type == NodeType.Union_SQLSTATEMENT:
        return visitor.query_nodes

    elif type == NodeType.ArithmeticExpression_EXPR:
        return visitor.all_arithmetic_nodes
    elif type == NodeType.MultiplyExpression_EXPR:
        return visitor.multi_nodes
    elif type == NodeType.DivideExpression_EXPR:
        return visitor.divide_nodes
    elif type == NodeType.ModuloExpression_EXPR:
        return visitor.modulo_nodes
    elif type == NodeType.AdditionExpression_EXPR:
        return visitor.add_nodes
    elif type == NodeType.SubtractionExpression_EXPR:
        return visitor.subtract_nodes

    elif type == NodeType.MapExpression_EXPR:
        return visitor.map_nodes


def replaceNode(src_node, after_node):
    if src_node is None:
        return
    parent_node = src_node.parent
    # src_node_type = src_node.type
    index = src_node.indexInParent

    if parent_node.type == NodeType.SelectItem_EXPR:
        parent_node.expr = after_node

    elif parent_node.type == NodeType.NameExpression_EXPR:
        parent_node.expr = after_node

    elif parent_node.type == NodeType.NestedExpression_EXPR:
        parent_node.expr = after_node

    elif parent_node.type == NodeType.LambdaExpression_EXPR:
        for ll in parent_node.left_list:
            if ll == src_node:
                parent_node.left_list[index] = after_node
                break
        if parent_node.right == src_node:
            parent_node.right = after_node

    elif NodeType.SqlAggFunction_EXPR.value <= parent_node.type.value < NodeType.ArithmeticExpression_EXPR.value:
        for arg in parent_node.args:
            if arg == src_node:
                parent_node.args[index] = after_node
                break

    elif parent_node.type == NodeType.NegateExpression_EXPR:
        parent_node.expr = after_node

    elif NodeType.MultiplyExpression_EXPR.value <= parent_node.type.value <= NodeType.SubtractionExpression_EXPR.value:
        if parent_node.left == src_node:
            parent_node.left = after_node
        else:
            parent_node.right = after_node

    elif parent_node.type == NodeType.IfExpression_EXPR or parent_node.type == NodeType.IIFFunction_EXPR:
        if parent_node.cond == src_node:
            parent_node.cond = after_node
        elif parent_node.then_expr == src_node:
            parent_node.then_expr = after_node
        else:
            parent_node.else_expr = after_node

    elif parent_node.type == NodeType.MultiIfExpression_EXPR:
        for arg in parent_node.args:
            if arg == src_node:
                parent_node.args[index] = after_node
                break

    elif parent_node.type == NodeType.CaseExpression_EXPR:
        if parent_node.case_expr == src_node:
            parent_node.case_expr = after_node
        for when_expr in parent_node.when_exprs:
            if when_expr == src_node:
                parent_node.when_exprs[index] = after_node
                break
        if parent_node.else_expr == src_node:
            parent_node.else_expr = after_node

    elif parent_node.type == NodeType.WhenExpression_EXPR:
        if parent_node.when_expr == src_node:
            parent_node.when_expr = after_node
        else:
            parent_node.then_expr = after_node

    elif parent_node.type == NodeType.TernaryExpression_EXPR:
        if parent_node.cond_expr == src_node:
            parent_node.cond_expr = after_node
        elif parent_node.then_expr == src_node:
            parent_node.then_expr = after_node
        else:
            parent_node.else_expr = after_node

    elif parent_node.type == NodeType.CommonFunction_EXPR:
        for cl in parent_node.column_list:
            if cl == src_node:
                parent_node.column_list[index] = after_node
                break
        for arg in parent_node.args:
            if arg == src_node:
                parent_node.args[index] = after_node
                break

    elif parent_node.type == NodeType.LogicalNot_EXPR or parent_node.type == NodeType.LogicalIsNull_EXPR:
        parent_node.expr = after_node

    elif NodeType.BinaryEqual_EXPR.value <= parent_node.type.value <= NodeType.LogicalLike_EXPR.value:
        if parent_node.left == src_node:
            parent_node.left = after_node
        else:
            parent_node.right = after_node

    elif parent_node.type == NodeType.LogicalBetween_EXPR:
        if parent_node.value == src_node:
            parent_node.value = after_node
        elif parent_node.lower_bound == src_node:
            parent_node.lower_bound = after_node
        else:
            parent_node.upper_bound = after_node

    else:
        logging.warning("current node not supported replace")
        return
