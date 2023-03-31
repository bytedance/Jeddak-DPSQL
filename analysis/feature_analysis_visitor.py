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
from parser.ast.type.node_type import NodeType, JoinKind
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor
from parser.ast.visitor.tree_visitor import VisitorOrder


class ComplexSqlAnalysis:
    """
        complex sql analysis.

    """

    def __init__(self, src_query):
        self.src_query = src_query
        self.agg_nodes = None
        self.analysis_center = None
        self._analysis()

    def _analysis(self):
        self.analysis_center = FeatureAnalysisCenter(self.src_query)
        self.analysis_center.analysis_basic_feature()

    def isNeedRewriteNoise(self):
        args_link_result = self.analysis_center.get_agg_args_link_agg()
        if len(args_link_result) > 0:
            msg = "There are aggregate function parameters that indirectly refer to other aggregate functions"
            return False, msg

        join_result = self.analysis_center.get_join_analysis_result()
        if len(join_result.nested_joins) > 0:
            msg = "There are nested joins or the number of consecutive joins is greater than two"
            return True, msg
        if join_result.cross_join_count > 0:
            msg = "There is a cross join"
            return True, msg

        arithmetic_agg_result = self.analysis_center.get_all_arithmetic_agg(self.analysis_center.root_scope_query, [1])
        if len(arithmetic_agg_result) > 0:
            msg = "Aggregation functions that participate in mathematical operations appear in the inner layer"
            return True, msg

        all_agg_nodes_result_1 = self.analysis_center.get_all_agg_nodes(self.analysis_center.root_scope_query, [1])
        all_agg_nodes_result_2 = self.analysis_center.get_all_agg_nodes_for_current_query(
            self.analysis_center.root_scope_query)

        if len(all_agg_nodes_result_1) > 1 and len(all_agg_nodes_result_2) == 0:
            msg = "The outermost layer has no aggregation function, and other layers have aggregation functions"
            return True, msg

        return False, "Minimum granularity limit, not open yet"

    def get_all_agg_nodes(self):
        if self.agg_nodes is None:
            self.agg_nodes = self.analysis_center.get_all_agg_nodes(self.analysis_center.root_scope_query, [])
        return self.agg_nodes


class ScopeQuery:
    """
        Query Hierarchical Relationship Analysis.

    """

    def __init__(self):
        self.level = 0
        self.select_block = None
        self.all_agg_func = []
        self.parent = None
        self.children = []
        # From left to right, only the one on the right is its brother, like a linked list
        self.brother = None
        # A new structure can be used to store this relationship
        self.brother_relation = None
        self.all_symbols = []
        self.all_agg_symbols = []


class FeatureAnalysisCenter:
    """
        Feature information analysis and store center

    """

    def __init__(self, src_query):
        self.src_query = src_query
        self.level_query = None
        self.level_symbol_info = []
        self.agg_args_info = []
        self.root_scope_query = None

    def analysis_query_scope(self):
        sav = ScopeAnalysisVisitor()
        self.src_query.accept(sav, VisitorOrder.SIMPLESEARCH)
        self.level_query = sav.levle_query
        self.root_scope_query = sav.root_scope_query

    def _analysis_symbol_scope(self):
        for item in self.level_query:
            # current_query = AstUtils.getCurrentQueryStatement(item[1])
            smv = SymbolMarkVisitor()
            item[1].accept(smv)
            self.level_symbol_info.append((item[0], smv))

    # Temporary workaround, further work required
    def _analysis_symbol_link(self):
        slv = SymbolLinkVisitor()
        self.src_query.accept(slv, VisitorOrder.SYMBOLLOADING)

    def get_agg_args_link_agg(self):
        aav = AggAnalysisVisitor()

        self._analysis_all_agg_symbol_feature(aav, self.root_scope_query)

        result = []
        for item in aav.analysis_info:
            if item not in result:
                result.append(item)

        return result

    def _analysis_all_agg_symbol_feature(self, aav, scope_query):
        if scope_query is None:
            return
        if scope_query.select_block is None:
            return

        scope_query.select_block.accept(aav)

        for item in scope_query.children:
            self._analysis_all_agg_symbol_feature(aav, item)

        if scope_query.brother is not None:
            scope_query.brother.select_block.accept(aav)

    def get_join_analysis_result(self):
        jav = JoinAnalysisVisitor()
        self.src_query.accept(jav)
        jav.analysisNestedJoin()

        return jav

    def get_all_arithmetic_agg(self, scope_query, filter_level):
        result = []

        if scope_query is None:
            return result
        if scope_query.select_block is None:
            return result

        if scope_query.level not in filter_level:
            for select_item in scope_query.select_block.nameExpressions:
                arithmetic_nodes = ast_utils.findNodes(select_item.expr, NodeType.ArithmeticExpression_EXPR)
                agg_nodes = ast_utils.findNodes(select_item.expr, NodeType.SqlAggFunction_EXPR)
                if len(arithmetic_nodes) > 0 and len(agg_nodes) > 0:
                    result.append(select_item)

        for item in scope_query.children:
            sub_result = self.get_all_arithmetic_agg(item, filter_level)
            result.extend(sub_result)

        if scope_query.brother is not None:
            brother_result = self.get_all_arithmetic_agg(scope_query.brother, filter_level)
            result.extend(brother_result)

        return self._remove_rebudant_item(result)

    def get_all_agg_nodes(self, scope_query, filter_list):
        result = []

        if scope_query.level not in filter_list:
            result.extend(self.get_all_agg_nodes_for_current_query(scope_query))

        for item in scope_query.children:
            sub_result = self.get_all_agg_nodes(item, filter_list)
            result.extend(sub_result)

        if scope_query.brother is not None:
            brother_result = self.get_all_agg_nodes(scope_query.brother, filter_list)
            result.extend(brother_result)

        return self._remove_rebudant_item(result)

    def get_all_agg_nodes_for_current_query(self, scope_query):
        result = []

        if scope_query is None:
            return result

        if scope_query.select_block is None:
            return result

        for select_item in scope_query.select_block.nameExpressions:
            agg_nodes = ast_utils.findNodes(select_item.expr, NodeType.SqlAggFunction_EXPR)
            if len(agg_nodes) > 0:
                result.extend(agg_nodes)

        return self._remove_rebudant_item(result)

    def is_in_m_symbols(self, node_name, m_symbols):
        for name, symbol in m_symbols:
            if node_name == name:
                return True
        return False

    def _remove_rebudant_item(self, src_list):
        result = []
        for item in src_list:
            if item not in result:
                result.append(item)

        return result

    def _extract_all_scope_query_symbol(self, scope_query):
        if scope_query is None:
            return

        if scope_query.select_block is None:
            # todo _extract_all_table_symbol()
            return

        for select_item in scope_query.select_block.nameExpressions:
            agg_nodes = ast_utils.findNodes(select_item, NodeType.SqlAggFunction_EXPR)
            if select_item.alias is not None:
                symbol_name = str(select_item.alias)
            else:
                symbol_name = str(select_item.expr)
            if len(agg_nodes) > 0 and self.is_in_m_symbols(symbol_name, scope_query.all_agg_symbols) is False:
                scope_query.all_agg_symbols.append((symbol_name, select_item.expr))

            if self.is_in_m_symbols(symbol_name, scope_query.all_symbols) is False:
                scope_query.all_symbols.append((symbol_name, select_item.expr))

        for item in scope_query.children:
            self._extract_all_scope_query_symbol(item)
        if scope_query.brother is not None:
            self._extract_all_scope_query_symbol(scope_query.brother)

    def _link_all_scope_query_symbol(self, scope_query):
        if scope_query is None:
            return

        for scope_item in scope_query.children:
            self._link_all_scope_query_symbol(scope_item)

        for symbol_item in scope_query.all_symbols:
            ssrv = ScopeSymbolRelationVisitor(scope_query)
            symbol_item[1].accept(ssrv)

        if scope_query.brother is not None:
            self._link_all_scope_query_symbol(scope_query.brother)

    def analysis_basic_feature(self):
        self.analysis_query_scope()
        self._extract_all_scope_query_symbol(self.root_scope_query)
        self._link_all_scope_query_symbol(self.root_scope_query)


class SymbolMarkVisitor(BaseAstVisitor):
    """
        Visitor iterate symbols and mark

    """

    def __init__(self):
        self.new_symbol = []
        self.new_symbol_contain_agg = []
        self.all_symbol = []

    def visitSelectItem(self, node):
        if node.alias is None:
            if self.is_in_m_symbols(str(node), self.all_symbol) is False:
                self.all_symbol.append((str(node), node.expr))
            return

        if self.is_in_m_symbols(str(node), self.new_symbol) is False:
            self.new_symbol.append((str(node.alias), node.expr))

        agg_nodes = ast_utils.findNodes(node.expr, NodeType.SqlAggFunction_EXPR)
        if len(agg_nodes) > 0:
            node.alias.state.agg_flag = True
            if self.is_in_m_symbols(str(node), self.new_symbol_contain_agg) is False:
                self.new_symbol_contain_agg.append((str(node.alias), node.expr))

        node.alias.state.src_expr.append(node.expr)

    def is_in_m_symbols(self, node_name, m_symbols):
        for name, symbol in m_symbols:
            if node_name == name:
                return True
        return False


class SymbolLinkVisitor(BaseAstVisitor):
    """
        Visitor traverse symbol and build connection

    """

    def visitSelectItem(self, node):

        current_query = ast_utils.getCurrentQueryStatement(node)
        current_with = current_query.with_block
        current_select = current_query.select_block
        current_source = current_query.source_block

        srv = SymbolRelationVisitor(current_with, current_select, current_source)
        node.expr.accept(srv)

        if node.alias is not None:
            node.alias.symbol = node.expr
            if self.is_in_m_symbols(str(node.alias), current_select.m_symbols) is False:
                current_select.m_symbols.append((str(node.alias), node.expr))
        else:
            if self.is_in_m_symbols(str(node), current_select.m_symbols) is False:
                current_select.m_symbols.append((str(node), node.expr))
                # if node.expr.type == NodeType.Identifier_EXPR:
                #     if
                #     current_select.m_symbols.append((str(node), node.expr.symbol))
                # else:
                #     current_select.m_symbols.append((str(node), node.expr))

    def is_in_m_symbols(self, node_name, m_symbols):
        for name, symbol in m_symbols:
            if node_name == name:
                return True
        return False


class ScopeSymbolRelationVisitor(BaseAstVisitor):
    """
        Visitor to create symbolic relationships by hierarchy

    """

    def __init__(self, scope_query):
        self.scope_query = scope_query

    def visitIdentifier(self, node):
        if node.state.symbol_link_flag is True:
            return
        self._loopFindSymbol(node, self.scope_query)
        node.state.symbol_link_flag = True

    def _loopFindSymbol(self, node, scope_query):
        if scope_query is None:
            return
        flag = self._findSymbol(node, scope_query)
        if flag is True:
            return

        if len(scope_query.children) == 0:
            return

        for item in scope_query.children:
            self._loopFindSymbol(node, item)

    def _findSymbol(self, node, scope_query):
        isFound = False
        if scope_query is None:
            return isFound

        node_name = str(node)

        if node.text is not None and "." in node.text:
            text_split = node.text.split(".")
            table_name = text_split[0]
            node_name = text_split[-1]

        for name, symbol in scope_query.all_symbols:
            if name == node_name:
                if str(symbol) == node_name:
                    continue

                node.state.src_expr.append(symbol)
                isFound = True
                break
        return isFound


class SymbolRelationVisitor(BaseAstVisitor):
    """
        Visitor to establish relationships between different types of nodes.

    """

    def __init__(self, withb, selectb, sourceb):
        self.withb = withb
        self.selectb = selectb
        self.sourceb = sourceb
        self.select_symbols = selectb.m_symbols
        self.with_symbols = ast_utils.getAllSymbolsFromWithBlock(withb)
        self.source_symbols = ast_utils.getAllSymbolsFromSourceBlock(sourceb)

    def visitIdentifier(self, node):
        node_name = str(node)
        src_select_symbols = self.select_symbols
        src_with_symbols = self.with_symbols
        src_source_symbols = self.source_symbols

        if node.text is not None and "." in node.text:
            text_split = node.text.split(".")
            table_name = text_split[0]
            node_name = text_split[-1]

            current_subquery_source = ast_utils.findTableFromSource(self.sourceb, table_name)
            src_source_symbols = ast_utils.getAllSymbolsFromSubquerySource(current_subquery_source)

        for name, symbol in src_select_symbols:
            if str(name) == node_name:
                node.state.src_expr.append(symbol)
        for name, symbol in src_with_symbols:
            if str(name) == node_name:
                node.state.src_expr.append(symbol)
        for name, symbol in src_source_symbols:
            if str(name) == node_name:
                node.state.src_expr.append(symbol)


class AggAnalysisVisitor(BaseAstVisitor):
    """
        Visitor to analysis aggregation type node.

    """

    def __init__(self):
        self.analysis_info = []

    def visitSelectItem(self, node):
        aaav = AggArgsAnalysisVisitor()
        node.expr.accept(aaav)
        nested_agg_info = aaav.nested_agg_info
        if len(nested_agg_info) > 0:
            self.analysis_info.append((node, nested_agg_info))

    # reserve : only for temp test
    def print_info(self):
        for item in self.analysis_info:
            current_query = ast_utils.getCurrentQueryStatement(item[0])
            print("It is found that the internal parameters of the aggregation function of the current query node directly or indirectly refer to other aggregation functions, the details are as follows： ")
            print("  query node expression： " + str(item[0]))
            print("  The main query list where the query node is located： " + str(current_query.select_block))
            print("  Problematic aggregate function for query nodes：")
            for agg_expr in item[1]:
                print("    " + str(agg_expr[0]))
                print("    The referenced aggregate function expressions have a total of " + str(len(agg_expr[1])) + " 个，具体如下 ：")
                for expr in agg_expr[1]:
                    print("      " + str(expr))


class AggArgsAnalysisVisitor(BaseAstVisitor):
    """
        Visitor to analysis aggregation type node's args.

    """

    def __init__(self):
        self.nested_agg_info = []

    def visitSqlCountFunction(self, node):
        if len(node.args) > 0:
            self.analysis(node, node.args[0])

    def visitSqlAvgFunction(self, node):
        self.analysis(node, node.args[0])

    def visitSqlMaxFunction(self, node):
        self.analysis(node, node.args[0])

    def visitSqlMinFunction(self, node):
        self.analysis(node, node.args[0])

    def visitSqlSumFunction(self, node):
        self.analysis(node, node.args[0])

    def visitSqlVarPopFunction(self, node):
        self.analysis(node, node.args[0])

    def visitSqlStdPopFunction(self, node):
        self.analysis(node, node.args[0])

    def analysis(self, node, arg):
        vav = VariableAnalysisVisitor()
        arg.accept(vav)
        agg_expr_list = vav.agg_expr_list
        if len(agg_expr_list) > 0:
            self.nested_agg_info.append((node, agg_expr_list))


class VariableAnalysisVisitor(BaseAstVisitor):
    """
        Visitor to analysis variable.

    """

    def __init__(self):
        self.agg_expr_list = []

    def visitIdentifier(self, node):
        if len(node.state.src_expr) == 0:
            return
        for expr in node.state.src_expr:
            agg_nodes = ast_utils.findNodes(expr, NodeType.SqlAggFunction_EXPR)
            if len(agg_nodes) > 0:
                self.agg_expr_list.extend(agg_nodes)
            else:
                # 间接关系传递暂不考虑
                pass


class ScopeAnalysisVisitor(BaseAstVisitor):
    """
         Strip its layers.

    """

    def __init__(self):
        self.level = 0
        self._subquery = 0
        self.levle_query = []
        self.current_level = [1]
        self.root_scope_query = None
        self._last_scope_query = None
        self._next_scope_query = None

    def visitSelectBlockStatement(self, node):
        if self.root_scope_query is None:
            self.root_scope_query = ScopeQuery()
            current_scope_query = self.root_scope_query
            current_scope_query.level = 1
        else:
            current_scope_query = self._next_scope_query

        current_query = ast_utils.getCurrentQueryStatement(node)
        self.level = self.current_level.pop()

        # current_scope_query.level = self.level
        current_scope_query.select_block = node
        self.levle_query.append((self.level, node))

        source_block = current_query.source_block

        if source_block is None:
            self._next_scope_query = self._getAnotherScope(current_scope_query)
            return
        if source_block.source.type == NodeType.SqlSubquerySource:
            self.current_level.append(self.level + 1)
            child_scope_query = ScopeQuery()
            child_scope_query.level = self.level + 1
            child_scope_query.parent = current_scope_query
            current_scope_query.children.append(child_scope_query)
            self._next_scope_query = child_scope_query
            self._last_scope_query = current_scope_query
        elif source_block.source.type == NodeType.SqlTableJoinSource:
            left_table = source_block.source.left_table
            join_count = self._getLeftTableJoinCount(left_table)
            self._last_scope_query = current_scope_query
            for i in range(join_count + 2):
                child_scope_query = ScopeQuery()
                child_scope_query.level = self.level + 1
                current_scope_query.children.append(child_scope_query)
                child_scope_query.parent = current_scope_query
                if i == 0:
                    self._next_scope_query = child_scope_query
                    temp_last_scope = child_scope_query
                else:
                    temp_last_scope.brother = child_scope_query
                    temp_last_scope = child_scope_query

                self.current_level.append(self.level + 1)
        elif source_block.source.type == NodeType.SqlTableSource:
            self._next_scope_query = self._getAnotherScope(current_scope_query)

    def _getLeftTableJoinCount(self, node):
        count = 0
        if node.type != NodeType.SqlTableJoinSource:
            return count
        count = count + 1
        left_table = node.left_table
        if left_table.type == NodeType.SqlTableJoinSource:
            sub_count = self._getLeftTableJoinCount(left_table)
            return count + sub_count
        else:
            return count

    def _getAnotherScope(self, current_scope_query):
        if current_scope_query is None:
            return None
        if current_scope_query.brother is not None:
            return current_scope_query.brother
        else:
            return self._getAnotherScope(current_scope_query.parent)


class SingleScopeAnalysisVisitor(BaseAstVisitor):
    """
         Analyze a single layer, analyze the characteristics of each layer.

    """

    def __init__(self):
        pass


class JoinAnalysisVisitor(BaseAstVisitor):
    """
         In-depth analysis of JOIN characteristics.

    """

    def __init__(self):
        self.join_count = 0
        self.join_part = []
        self.joins = []
        self.nested_joins = []
        self.cross_join_count = 0

    def visitSqlTableJoinSource(self, node):
        self.join_count = self.join_count + 1
        self.join_part.append((node.left_table, node.right_table))
        self.joins.append(node)
        if node.join_type.kind == JoinKind.Cross:
            self.cross_join_count = self.cross_join_count + 1

    def analysisNestedJoin(self):
        for item in self.joins:
            left_table = item.left_table
            right_table = item.right_table
            jav = JoinAnalysisVisitor()
            left_table.accept(jav)
            if jav.join_count > 0:
                self.nested_joins.append(item)
                continue
            right_table.accept(jav)
            if jav.join_count > 0:
                self.nested_joins.append(item)
