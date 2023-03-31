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

from parser.ast.expr.function_expr import MATH_FUNCTION
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor


class AggFunctionFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.all_agg_nodes = []
        self.agg_nodes = []
        self.count_nodes = []
        self.min_nodes = []
        self.max_nodes = []
        self.sum_nodes = []
        self.avg_nodes = []
        self.var_pop_nodes = []
        self.var_samp_nodes = []
        self.std_pop_nodes = []
        self.std_samp_nodes = []

    def visitSqlAggFunction(self, node):
        self.agg_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlCountFunction(self, node):
        self.count_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlMinFunction(self, node):
        self.min_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlMaxFunction(self, node):
        self.max_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlSumFunction(self, node):
        self.sum_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlAvgFunction(self, node):
        self.avg_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlVarPopFunction(self, node):
        self.var_pop_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlVarSampFunction(self, node):
        self.var_samp_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlStdPopFunction(self, node):
        self.std_pop_nodes.append(node)
        self.all_agg_nodes.append(node)

    def visitSqlStdSampFunction(self, node):
        self.std_samp_nodes.append(node)
        self.all_agg_nodes.append(node)


class BooleanExpressionFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.binary_equal_nodes = []
        self.logical_equal_nodes = []
        self.logical_not_nodes = []
        self.logical_and_nodes = []
        self.logical_or_nodes = []
        self.logical_concat_nodes = []
        self.logical_is_null_nodes = []
        self.logical_compare_nodes = []
        self.logical_in_nodes = []
        self.logical_like_nodes = []
        # self.logical_between_nodes = []
        self.all_nodes = []

    def visitBinaryEqual(self, node):
        self.binary_equal_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalEqual(self, node):
        self.logical_equal_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalNot(self, node):
        self.logical_not_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalAnd(self, node):
        self.logical_and_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalOr(self, node):
        self.logical_or_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalConcat(self, node):
        self.logical_concat_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalIsNull(self, node):
        self.logical_is_null_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalCompare(self, node):
        self.logical_compare_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalIn(self, node):
        self.logical_in_nodes.append(node)
        self.all_nodes.append(node)

    def visitLogicalLike(self, node):
        self.logical_like_nodes.append(node)
        self.all_nodes.append(node)

    # def visitLogicalBetween(self, node):
    #     self.logical_between_nodes.append(node)


class CondFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.if_nodes = []
        self.iif_nodes = []
        self.multiif_nodes = []
        self.case_nodes = []
        self.when_nodes = []
        self.ternary_nodes = []
        self.all_nodes = []

    def visitIfExpression(self, node):
        self.if_nodes.append(node)
        self.all_nodes.append(node)

    def visitIIFFunction(self, node):
        self.iif_nodes.append(node)
        self.all_nodes.append(node)

    def visitMultiIfExpression(self, node):
        self.multiif_nodes.append(node)
        self.all_nodes.append(node)

    def visitCaseExpression(self, node):
        self.case_nodes.append(node)
        self.all_nodes.append(node)

    def visitWhenExpression(self, node):
        self.when_nodes.append(node)
        self.all_nodes.append(node)

    def visitTernaryExpression(self, node):
        self.ternary_nodes.append(node)
        self.all_nodes.append(node)


# todo : To be perfected
class FunctionFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.all_func_nodes = []
        self.common_func_nodes = []
        self.math_func_nodes = []

    def visitCommonFunction(self, node):

        if node.func_name.upper() in MATH_FUNCTION:
            self.math_func_nodes.append(node)
        else:
            self.common_func_nodes.append(node)

        self.all_func_nodes.append(node)

    def visitMathFunction(self, node):
        pass


class SqlQueryFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.query_nodes = []

    def visitUnionSelectStatement(self, node):
        self.query_nodes.append(node)


# todo : To be perfected
class SqlSourceFinderVisitor(BaseAstVisitor):

    def __init__(self):
        self.all_source_nodes = []
        self.table_source_nodes = []
        self.table_join_source_nodes = []
        # self.table_union_source_nodes = []
        self.subquery_source_nodes = []
        # self.array_join_source_nodes = []
        self.fusion_merge_source_nodes = []

    def visitSqlTableSource(self, node):
        self.table_source_nodes.append(node)
        self.all_source_nodes.append(node)

    def visitSqlTableJoinSource(self, node):
        self.table_join_source_nodes.append(node)
        self.all_source_nodes.append(node)

    def visitSqlSubquerySource(self, node):
        self.subquery_source_nodes.append(node)
        self.all_source_nodes.append(node)

    def visitFusionMergeSource(self, node):
        self.fusion_merge_source_nodes.append(node)
        self.all_source_nodes.append(node)


class ArithmeticFinderVisitor(BaseAstVisitor):
    def __init__(self):
        self.all_arithmetic_nodes = []
        self.multi_nodes = []
        self.divide_nodes = []
        self.add_nodes = []
        self.subtract_nodes = []
        self.modulo_nodes = []

    def visitMultiplyExpression(self, node):
        self.multi_nodes.append(node)
        self.all_arithmetic_nodes.append(node)

    def visitDivideExpression(self, node):
        self.divide_nodes.append(node)
        self.all_arithmetic_nodes.append(node)

    def visitAdditionExpression(self, node):
        self.add_nodes.append(node)
        self.all_arithmetic_nodes.append(node)

    def visitModuloExpression(self, node):
        self.modulo_nodes.append(node)
        self.all_arithmetic_nodes.append(node)

    def visitSubtractionExpression(self, node):
        self.subtract_nodes.append(node)
        self.all_arithmetic_nodes.append(node)


class BaseExprFinderVisitor(BaseAstVisitor):
    def __init__(self):
        self.map_nodes = []

    def visitMapExpression(self, node):
        self.map_nodes.append(node)















