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

from parser.utils import ast_utils
from parser.ast.expr.agg_function_expr import SqlSumFunction, SqlCountFunction
from parser.ast.expr.arithmetic_expr import DivideExpression, MultiplyExpression, SubtractionExpression
from parser.ast.expr.base_expr import NestedExpression
from parser.ast.expr.function_expr import MathFunction
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor


class RewriteBasedRewriter:
    def __init__(self, input_ast):
        self.ast = input_ast
        self.rewirter = RewriteBasedVisitor()

    def rewrite(self, input_ast=None):
        if input_ast is None:
            self.ast.accept(self.rewirter)
        else:
            input_ast.accept(self.rewirter)
        return self.ast


class RewriteBasedVisitor(BaseAstVisitor):

    def visitSqlAggFunction(self, node):
        pass

    def visitSqlAvgFunction(self, node):
        ssf = SqlSumFunction()
        scf = SqlCountFunction()

        for arg in node.args:
            arg1 = arg.clone()
            arg2 = arg.clone()
            ssf.args.append(arg1)
            scf.args.append(arg2)

        de = DivideExpression(ssf, scf)

        ne = NestedExpression()
        ne.expr = de

        ast_utils.replaceAstNode(node, ne)
        #
        # if node.parent.type == NodeType.SelectItem_EXPR:
        #     node.parent.alias = Identifier(str(node))

    def visitSqlVarPopFunction(self, node):
        ne = self._buildVapPopExpression(node)
        ast_utils.replaceAstNode(node, ne)

    def visitSqlStdPopFunction(self, node):
        var_node = self._buildVapPopExpression(node)
        mf = MathFunction("SQRT")
        mf.args.append(var_node)

        ast_utils.replaceAstNode(node, mf)

    def _buildVapPopExpression(self, node):
        ssf = SqlSumFunction()
        scf = SqlCountFunction()
        ssf2 = SqlSumFunction()
        scf2 = SqlCountFunction()

        for arg in node.args:
            ssf.args.append(arg.clone())
            scf.args.append(arg.clone())

            eexpr = MultiplyExpression(arg.clone(), arg.clone())
            ssf2.args.append(eexpr)
            scf2.args.append(eexpr.clone())

        de1 = DivideExpression(ssf2, scf2)
        de2 = DivideExpression(ssf, scf)
        me = MultiplyExpression(de2, de2)
        se = SubtractionExpression(de1, me)

        ne = NestedExpression()
        ne.expr = se

        return ne

    # def visitSqlVarSampFunction(self, node):
    #     pass

    # def visitSqlStdSampFunction(self, node):
    #     pass
