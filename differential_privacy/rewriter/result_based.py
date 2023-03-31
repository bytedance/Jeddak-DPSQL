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
from parser.ast.base import Seq
from parser.ast.expr.agg_function_expr import SqlSumFunction, SqlCountFunction
from parser.ast.expr.arithmetic_expr import MultiplyExpression, DivideExpression, SubtractionExpression
from parser.ast.expr.base_expr import SelectItem, Identifier, NestedExpression
from parser.ast.expr.function_expr import MathFunction
from parser.ast.statement.block_statement import SelectBlockStatement, FromBlockStatement
from parser.ast.statement.select_statement import ByteClickHouseSelectStatement, SelectUnionStatement
from parser.ast.tablesource.table_source import SqlSubquerySource
from parser.ast.type.node_type import NodeType
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor
import random
import string


class ResultBasedRewriter:
    def __init__(self, input_ast):
        self.ast = input_ast
        self.rewirter = ResultBasedVisitor()
        self.clipping_rewriter = None

    def rewrite(self):
        self.ast.accept(self.rewirter)

        # start rewrite for clipping
        inner_query = self.get_inner_query()

        self.clipping_rewriter = RewriterClippingVisitor()
        inner_query.accept(self.clipping_rewriter)

        return self

    def get_result(self):
        return self.rewirter.get_result()

    def get_inner_query(self):
        return self.rewirter.get_inner_query()

    def fix(self):
        self.rewirter.fixGroupKey()


class ResultBasedVisitor(BaseAstVisitor):

    def __init__(self):
        self.parse_pre_flag = False
        self.parse_post_flag = False
        self.inner_query = None
        self.inner_query_new_nameExpressions = None
        self.outer_query = self.buildOuterQuery()
        # # execute the rewriter
        # ast.accept(self)

    def get_result(self):
        return self.outer_query

    def get_inner_query(self):
        return self.inner_query

    def postVisitSelectBlockStatement(self, node):

        if self.parse_post_flag:
            return
        else:
            self.parse_post_flag = True

            self.inner_query.select_block.nameExpressions = self.inner_query_new_nameExpressions

            sus = SelectUnionStatement()
            sus.select_statements.append(self.inner_query)

            sss = SqlSubquerySource(sus)
            sss.alias = Identifier("exact_aggregates")
            fb = FromBlockStatement()
            fb.source = sss
            self.outer_query.source_block = fb
            self.outer_query.groupBy_block = self.inner_query.groupBy_block
            # self.fixOutSymbols()
            self.fixGroupKey()

    # def fixOutSymbols(self):
    #     outer_select_block = self.outer_query.select_block
    #     for item in outer_select_block.nameExpressions:
    #         if item.alias is not None:
    #             item.alias.symbol = item.expr
    #             outer_select_block.m_symbols.append((str(item.alias), item.expr))
    #         else:
    #             outer_select_block.m_symbols.append((str(item.expr), item.expr))
    #
    #     outer_source_block = self.outer_query.source_block
    #     outer_source_block.m_symbols = []
    #     if self.inner_query.with_block is not None:
    #         outer_source_block.m_symbols.extend(self.inner_query.with_block.m_symbols)
    #     outer_source_block.m_symbols.extend(self.inner_query.select_block.m_symbols)

    def fixGroupKey(self):
        query = self.outer_query
        select_block_symbols = query.select_block.m_symbols
        if query.groupBy_block is None:
            return

        group_list = query.groupBy_block.group_expressions

        for item in group_list:
            for symbol in select_block_symbols:
                if str(item) == symbol[0]:
                    symbol[1].is_group_key = True

    def visitSelectBlockStatement(self, node):
        if self.parse_pre_flag:
            return
        else:
            self.parse_pre_flag = True
            self.inner_query_new_nameExpressions = Seq(node)
            self.inner_query = ast_utils.getCurrentQueryStatement(node)

    def visitSelectItem(self, node):
        if self.parse_post_flag:
            return

        agg_nodes = ast_utils.findNodes(node, NodeType.SqlAggFunction_EXPR)

        if node.expr.type == NodeType.SqlVarPopFunction_EXPR:
            self.rewriteVarPopFunction(node.expr, node.alias)
        elif node.expr.type == NodeType.SqlStdPopFunction_EXPR:
            self.rewriteStdPopFunction(node.expr, node.alias)
        elif node.expr.type == NodeType.SqlAvgFunction_EXPR:
            self.rewriteAvgFunction(node.expr, node.alias)
        elif node.expr.type == NodeType.SqlSumFunction_EXPR:
            self.rewriteSumFunction(node.expr, node.alias)
        elif node.expr.type == NodeType.SqlCountFunction_EXPR:
            self.rewriteCountFunction(node.expr, node.alias)
        elif len(agg_nodes) > 0:
            self.rewriteNestedAggFunction(node.expr, node.alias)
            # split_visitor = RewriteBasedRewriter()
            # node.accept(split_visitor)
            # self.rewriteOthers(node.expr, node.alias)
        else:
            self.rewriteOthers(node.expr, node.alias)

    def rewriteVarPopFunction(self, node, alias):

        si1, si2, si3 = self.splitNode(node)

        outer_var = self.buildVarAstNode(si1.alias, si2.alias, si3.alias)
        si = SelectItem()
        ne = NestedExpression()
        ne.expr = outer_var
        si.expr = ne
        # si.alias = alias.clone() if alias is not None else None
        if alias is None:
            alias_ident = Identifier(str(node))
            alias_ident.symbol = si.expr
            si.alias = alias_ident
        else:
            si.alias = alias.clone()

        self.outer_query.select_block.nameExpressions.append(si)

    def rewriteStdPopFunction(self, node, alias):
        si1, si2, si3 = self.splitNode(node)

        outer_var = self.buildStdAstNode(si1.alias, si2.alias, si3.alias)
        si = SelectItem()
        ne = NestedExpression()
        ne.expr = outer_var
        si.expr = ne
        # si.alias = alias.clone() if alias is not None else None
        if alias is None:
            alias_ident = Identifier(str(node))
            alias_ident.symbol = si.expr
            si.alias = alias_ident
        else:
            si.alias = alias.clone()

        self.outer_query.select_block.nameExpressions.append(si)

    def rewriteAvgFunction(self, node, alias):
        si1, si2 = self.splitNode2(node)
        outer_avg = self.buildAvgAstNode(si1.alias, si2.alias)

        si = SelectItem()
        ne = NestedExpression()
        ne.expr = outer_avg
        si.expr = ne
        # si.alias = alias.clone() if alias is not None else None
        if alias is None:
            alias_ident = Identifier(str(node))
            alias_ident.symbol = si.expr
            si.alias = alias_ident
        else:
            si.alias = alias.clone()

        self.outer_query.select_block.nameExpressions.append(si)
        self.fixInnerSymbols(node, alias, si1, si2)

    def rewriteSumFunction(self, node, alias):
        si = self.getNode(node)
        if si is None:
            si = SelectItem()
            si.expr = node
            # si.alias = alias.clone() if alias is not None else None
            if alias is None:
                rand_str = "".join(random.choice(string.ascii_letters) for i in range(7))
                text = "sum_%s" % rand_str
                alias_ident = Identifier(text)
                alias_ident.symbol = si.expr
                si.alias = alias_ident
            else:
                si.alias = alias.clone()
            self.inner_query_new_nameExpressions.append(si)

        osi = SelectItem()
        if si.alias is not None:
            osi.expr = si.alias
            alias_ident = Identifier(str(node))
            alias_ident.symbol = osi.expr
            osi.alias = alias_ident
        else:
            osi.expr = si.expr
            osi.alias = None
        self.outer_query.select_block.nameExpressions.append(osi)

    def rewriteCountFunction(self, node, alias):
        si = self.getNode(node)
        if si is None:
            si = SelectItem()
            si.expr = node
            # si.alias = alias.clone() if alias is not None else None
            if alias is None:
                rand_str = "".join(random.choice(string.ascii_letters) for i in range(7))
                text = "sum_%s" % rand_str
                alias_ident = Identifier(text)
                alias_ident.symbol = si.expr
                si.alias = alias_ident
            else:
                si.alias = alias.clone()

            self.inner_query_new_nameExpressions.append(si)

        osi = SelectItem()
        if si.alias is not None:
            osi.expr = si.alias
            alias_ident = Identifier(str(node))
            alias_ident.symbol = osi.expr
            osi.alias = alias_ident
        else:
            osi.expr = si.expr
            osi.alias = None
        self.outer_query.select_block.nameExpressions.append(osi)

    def rewriteNestedNoSplitAggFunction(self, node, alias):
        if alias is not None:
            self.rewriteOthers(node, alias)
            return
        if node.type.value > NodeType.SubtractionExpression_EXPR.value or node.type.value < NodeType.MultiplyExpression_EXPR.value:
            self.rewriteOthers(node, alias)
            return

        rand_str = "".join(random.choice(string.ascii_letters) for i in range(7))
        alias = Identifier(rand_str)
        alias.symbol = node
        self.rewriteOthers(node, alias)

    def rewriteNestedAggFunction(self, node, alias):
        avg_nodes = ast_utils.findNodes(node, NodeType.SqlAvgFunction_EXPR)
        varPop_nodes = ast_utils.findNodes(node, NodeType.SqlVarPopFunction_EXPR)
        stdPop_nodes = ast_utils.findNodes(node, NodeType.SqlStdPopFunction_EXPR)

        if len(avg_nodes) > 1 or len(varPop_nodes) > 1 or len(stdPop_nodes) > 1 or len(avg_nodes) + len(varPop_nodes) + len(stdPop_nodes) == 0:
            self.rewriteNestedNoSplitAggFunction(node, alias)
            return

        for avg_node in avg_nodes:
            si1, si2 = self.splitNode2(avg_node)
            devide_avg = self.buildAvgAstNode(si1.alias, si2.alias)
            ne = NestedExpression()
            ne.expr = devide_avg
            self.fixInnerSymbols(avg_node, None, si1, si2)

            ast_utils.replaceAstNode(avg_node, ne)

        for var_node in varPop_nodes:
            si1, si2, si3, si4 = self.splitNode(var_node)
            devide_var = self.buildVarAstNode(si1.alias, si2.alias, si3.alias, si4.alias)
            ne = NestedExpression()
            ne.expr = devide_var

            ast_utils.replaceAstNode(var_node, ne)

        for std_node in stdPop_nodes:
            si1, si2, si3, si4 = self.splitNode(std_node)
            devide_std = self.buildStdAstNode(si1.alias, si2.alias, si3.alias, si4.alias)
            ne = NestedExpression()
            ne.expr = devide_std

            ast_utils.replaceAstNode(std_node, ne)

        si = SelectItem()
        si.expr = node.clone()
        si.alias = alias.clone() if alias is not None else None
        self.outer_query.select_block.nameExpressions.append(si)

    def fixInnerSymbols(self, node, alias, si1, si2):
        src_m_symbols = self.inner_query.select_block.m_symbols.copy()
        self.inner_query.select_block.m_symbols = []
        if len(src_m_symbols) == 0:
            return

        if alias is not None:
            src_name = str(alias)
        else:
            src_name = str(node)

        for item in src_m_symbols:
            if item[0] == src_name:
                self.inner_query.select_block.m_symbols.append((str(si1.alias), si1.expr))
                self.inner_query.select_block.m_symbols.append((str(si2.alias), si2.expr))
            else:
                self.inner_query.select_block.m_symbols.append((item[0], item[1]))
        si1.alias.symbol = si1.expr
        si2.alias.symbol = si2.expr

    def rewriteOthers(self, node, alias):

        rev = RewriterExpandVisitor(self.outer_query.select_block.nameExpressions)
        node.accept(rev)

        si = self.getNode(node)
        if si is None:
            si = SelectItem()
            si.expr = node
            si.alias = alias.clone() if alias is not None else None
            self.inner_query_new_nameExpressions.append(si)

        osi = SelectItem()
        if si.alias is not None:
            osi.expr = si.alias.clone()
            alias_ident = Identifier(alias.text)
            alias_ident.symbol = osi.expr
            osi.alias = alias_ident
        else:
            osi.expr = si.expr
            osi.alias = None
        self.outer_query.select_block.nameExpressions.append(osi)

    def getNode(self, node):
        for ne in self.inner_query_new_nameExpressions:
            if str(node) == str(ne.expr):
                return ne
        return None

    def buildOuterQuery(self):
        query = ByteClickHouseSelectStatement()
        query.select_block = SelectBlockStatement()

        return query

    def buildVarAstNode(self, sum_var1, count_var1, sum_var2):
        de1 = DivideExpression(sum_var2, count_var1)
        de2 = DivideExpression(sum_var1, count_var1)
        me = MultiplyExpression(de2, de2)
        se = SubtractionExpression(de1, me)
        return se

    def buildStdAstNode(self, sum_var1, count_var1, sum_var2):
        var_node = self.buildVarAstNode(sum_var1, count_var1, sum_var2)
        mf = MathFunction("SQRT")
        mf.args.append(var_node)
        return mf

    def buildAvgAstNode(self, sum_var, count_var):
        de = DivideExpression(sum_var, count_var)
        return de

    def splitNode(self, node):
        ssf = SqlSumFunction()
        scf = SqlCountFunction()
        ssf2 = SqlSumFunction()

        for arg in node.args:
            ssf.args.append(arg.clone())
            scf.args.append(arg.clone())

            eexpr = MultiplyExpression(arg.clone(), arg.clone())
            ssf2.args.append(eexpr)

        si1 = self.getNode(ssf)
        si2 = self.getNode(scf)
        si3 = self.getNode(ssf2)

        rand_str = "".join(random.choice(string.ascii_letters) for i in range(7))
        if si1 is None:
            si1 = SelectItem()
            si1.expr = ssf
            text = "sum_%s" % rand_str
            si1.alias = Identifier(text)
            self.inner_query_new_nameExpressions.append(si1)

        if si2 is None:
            si2 = SelectItem()
            si2.expr = scf
            text = "count_%s" % rand_str
            si2.alias = Identifier(text)
            self.inner_query_new_nameExpressions.append(si2)

        rand_str2 = "".join(random.choice(string.ascii_letters) for i in range(7))
        if si3 is None:
            si3 = SelectItem()
            si3.expr = ssf2
            text = "sum_%s" % rand_str2
            si3.alias = Identifier(text)
            self.inner_query_new_nameExpressions.append(si3)

        return si1, si2, si3

    def splitNode2(self, node):
        ssf = SqlSumFunction()
        scf = SqlCountFunction()

        for arg in node.args:
            ssf.args.append(arg.clone())
            scf.args.append(arg.clone())

        si1 = self.getNode(ssf)
        si2 = self.getNode(scf)

        rand_str = "".join(random.choice(string.ascii_letters) for i in range(7))
        if si1 is None:
            si1 = SelectItem()
            si1.expr = ssf
            text = "sum_%s" % rand_str
            si1.alias = Identifier(text)
            self.inner_query_new_nameExpressions.append(si1)

        if si2 is None:
            si2 = SelectItem()
            si2.expr = scf
            text = "count_%s" % rand_str
            si2.alias = Identifier(text)
            self.inner_query_new_nameExpressions.append(si2)

        return si1, si2


class RewriterExpandVisitor(BaseAstVisitor):

    def __init__(self, outer_nameExpressions):
        self.outer_nameExpressions = outer_nameExpressions

    def visitIdentifier(self, node):
        for item in self.outer_nameExpressions:
            if item.alias is not None and str(node) == str(item.alias):
                ast_utils.replaceAstNode(node, item.expr.clone())


class RewriterClippingVisitor(ResultBasedVisitor):

    def __init__(self):
        super(RewriterClippingVisitor, self).__init__()

    def rewriteSumFunction(self, node, alias):
        rev = RewriterClippingExpandVisitor()
        node.accept(rev)
        si = self.getNode(node)
        if si is None:
            si = SelectItem()
            si.expr = node.clone()
            if alias is not None:
                si.alias = alias.clone()
            self.inner_query_new_nameExpressions.append(si)


class RewriterClippingExpandVisitor(ResultBasedVisitor):

    def __init__(self):
        super(RewriterClippingExpandVisitor, self).__init__()

    def visitIdentifier(self, node):
        symbol = node.symbol
        clipping_flag = None
        maxval = None
        minval = None
        ident_str = None
        if hasattr(symbol, "clipping_flag"):
            clipping_flag = symbol.clipping_flag

        if hasattr(symbol, "maxval"):
            maxval = symbol.maxval
        if hasattr(symbol, "minval"):
            minval = symbol.minval
        if hasattr(symbol, "name"):
            ident_str = symbol.name

        if clipping_flag:
            expr_dict = {
                "clipping_upper": maxval,
                "clipping_lower": minval,
                "ident_str": ident_str
            }

            clipping_expr_str = '''
            CASE WHEN {ident_str} >= {clipping_upper} THEN {clipping_upper}
            WHEN {ident_str} <= {clipping_lower} THEN {clipping_lower}
            ELSE {ident_str}
            END
            '''.format(**expr_dict)
            clipping_node = ast_utils.createExprNode(clipping_expr_str)
            ast_utils.replaceAstNode(node, clipping_node.clone())
