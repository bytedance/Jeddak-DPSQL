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
# External interface for AST operations

import logging

from parser.ast.builder.hive_query_ast_builder import HiveAstBuilder
from parser.search.node_finder import replaceNode, findVisitorNodes
from parser.ast.base import SqlNode
from parser.ast.builder import block_ast_builder
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder
from parser.ast.dialect.clickhouse.clickhouse_writter import ClickHousePrinter
from parser.ast.dialect.hive.hive_writer import HivePrinter
from parser.ast.type.node_type import DialectType, NodeType

# 用于判断当前节点是否为聚合函数
from parser.search.nodes_finder_visitor import AggFunctionFinderVisitor, CondFinderVisitor, \
    BooleanExpressionFinderVisitor, FunctionFinderVisitor, SqlSourceFinderVisitor, SqlQueryFinderVisitor, \
    ArithmeticFinderVisitor, BaseExprFinderVisitor


# Complete AST tree conversion, local node conversion is also considered to support
def tosql(ast, dialect=None):
    if dialect == DialectType.CLICKHOUSE:
        printer = ClickHousePrinter(ast)
        return printer.print()
    elif dialect == DialectType.HIVE:
        printer = HivePrinter(ast)
        return printer.print()
    # if dialect == DialectType.MYSQL:
    #     return "MYSQL"
    # elif dialect == DialectType.ORACLE:
    #     return "ORACLE"
    else:
        return "UnSupported"


# Determine whether the current node is an aggregation node
def isAggFunction(node):
    if not isinstance(node, SqlNode):
        return False
    if node.type.value < NodeType.SqlAggFunction_EXPR.value:
        return False
    elif node.type.value >= NodeType.ArithmeticExpression_EXPR.value:
        return False
    else:
        return True


# Used to get the Query statement to which the current node belongs
def getCurrentQueryStatement(node):
    if node.type.value < NodeType.Common_SQLSTATEMENT.value:
        return None
    elif node.type.value >= NodeType.BLOCKSTATEMENT.value:
        return getCurrentQueryStatement(node.parent)
    else:
        return node


# Get the select item node to which the current node belongs
def getCurrentSelectItem(node):
    if node.type.value < NodeType.EXPR.value or node.type.value >= NodeType.SqlSource.value:
        return None
    elif node.type.value == NodeType.SelectItem_EXPR:
        return node
    else:
        return getCurrentSelectItem(node.parent)


# Get the alias of the current query
def getCurrentQueryAlias(node):
    if node is None:
        return None

    if NodeType.SqlSource.value < node.type.value <= NodeType.SqlFusionMergeSource.value:
        return node.alias

    if node.parent is None:
        return None
    else:
        return getCurrentQueryAlias(node.parent)


# Used to find a table from a specified data source
def findTableFromSource(source_node, table_name):
    source = source_node
    if source_node.type == NodeType.From_BLOCKSTATEMENT:
        source = source_node.source

    if source.type == NodeType.SqlTableJoinSource:
        left_table = source.left_table
        right_table = source.right_table
        target_table = findTableFromSource(left_table, table_name)
        if target_table is not None:
            return target_table
        target_table = findTableFromSource(right_table, table_name)
        if target_table is not None:
            return target_table

    if source.type == NodeType.SqlSubquerySource:
        if source.alias is not None and str(source.alias) == table_name:
            return source

    if source.type == NodeType.SqlTableSource:
        if source.alias is not None and str(source.alias) == table_name:
            return source
        if str(source.table_expr) == table_name:
            return source

    return None


# Used to get the Block Statement to which the current node belongs
def getCurrentBlockStatement(node):
    if node.type == NodeType.Union_SQLSTATEMENT and node.parent is None:
        return None
    elif NodeType.BLOCKSTATEMENT.value < node.type.value < NodeType.EXPR.value:
        return node
    else:
        return getCurrentBlockStatement(node.parent)


# Get the specified target type block of the query where the current node is located
def getCurrentOtherBlock(source_block, target_type):
    if source_block.type.value < NodeType.BLOCKSTATEMENT.value or source_block.type.value >= NodeType.EXPR.value:
        return None

    if target_type.value < NodeType.BLOCKSTATEMENT.value or target_type.value >= NodeType.EXPR.value:
        return None

    if target_type == NodeType.From_BLOCKSTATEMENT:
        return source_block.parent.source_block


# Used to extract all symbol information from the from block
def getAllSymbolsFromSourceBlock(node):
    symbols = []
    if node is None or node.type != NodeType.From_BLOCKSTATEMENT:
        return symbols
    source_type = node.source.type
    if source_type == NodeType.SqlTableSource:
        table = node.source.table_expr
        for column in table.columns:
            symbols.append((column.name, column))
    elif source_type == NodeType.SqlSubquerySource:
        sub_querys = node.source.select_query.select_statements
        for query in sub_querys:
            if query.with_block is not None:
                symbols.extend(getAllSymbolsFromWithBlock(query.with_block))
            if query.select_block is not None:
                symbols.extend(query.select_block.m_symbols)
            # if query.source_block is not None:
            #     symbols.extend(query.source_block.m_symbols)
    elif source_type == NodeType.SqlTableJoinSource:
        symbols = getAllSymbolsFromSqlTableJoinSource(node.source)
    else:
        pass
    node.m_symbols = symbols
    return symbols


def getAllSymbolsFromSubquerySource(node):
    if node.type != NodeType.SqlSubquerySource:
        return None

    symbols = []
    sub_querys = node.select_query.select_statements
    for query in sub_querys:
        if query.with_block is not None:
            symbols.extend(getAllSymbolsFromWithBlock(query.with_block))
        if query.select_block is not None:
            symbols.extend(query.select_block.m_symbols)
        # if query.source_block is not None:
        #     symbols.extend(getAllSymbolsFromSourceBlock(query.source_block))

    return symbols


def getAllSymbolsFromSqlTableJoinSource(node):
    symbols = []
    if node.left_table.type == NodeType.SqlTableSource:
        left_table = node.left_table.table_expr
        for column in left_table.columns:
            symbols.append((column.name, column))
    elif node.left_table.type == NodeType.SqlSubquerySource:
        left_symbols = getAllSymbolsFromSubquerySource(node.left_table)
        symbols.extend(left_symbols)
    else:
        left_symbols = getAllSymbolsFromSqlTableJoinSource(node.left_table)
        symbols.extend(left_symbols)

    if node.right_table.type == NodeType.SqlTableSource:
        right_table = node.right_table.table_expr
        for column in right_table.columns:
            symbols.append((column.name, column))
    elif node.right_table.type == NodeType.SqlSubquerySource:
        right_symbols = getAllSymbolsFromSubquerySource(node.right_table)
        symbols.extend(right_symbols)
    else:
        right_symbols = getAllSymbolsFromSqlTableJoinSource(node.right_table)
        symbols.extend(right_symbols)
    return symbols


def getAllSymbolsFromWithBlock(node):
    symbols = []
    return symbols


# def getAllSymbolsFromSelectBlock(node):
#     symbols = []
#     return symbols


# Create an expression ast node
def createExprNode(src, target_type=DialectType.CLICKHOUSE):
    if target_type == DialectType.CLICKHOUSE:
        builder = ClickHouseAstBuilder()
        ast = builder.get_expr_ast(src)
    elif target_type == DialectType.HIVE:
        builder = HiveAstBuilder()
        ast = builder.get_expr_ast(src)
    else:
        ast = None
    return ast


# Create a block ast node, temporarily only supports clickhouse
def createBlockNode(src, node_type, target_type=DialectType.CLICKHOUSE):
    if target_type != target_type == DialectType.CLICKHOUSE:
        return None
    if node_type == NodeType.With_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseWithBlockAst(src)
    elif node_type == NodeType.Select_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseSelectBlockAst(src)
    elif node_type == NodeType.From_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseFromBlockAst(src)
    elif node_type == NodeType.Where_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseWhereBlockAst(src)
    elif node_type == NodeType.GroupBy_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseGroupByBlockAst(src)
    elif node_type == NodeType.Having_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseHavingBlockAst(src)
    elif node_type == NodeType.OrderBy_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseOrderByBlockAst(src)
    elif node_type == NodeType.Limit_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseLimitBlockAst(src)
    elif node_type == NodeType.LimitBy_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseLimitByBlockAst(src)
    elif node_type == NodeType.TeaLimit_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseTeaLimitBlockAst(src)
    elif node_type == NodeType.Settings_BLOCKSTATEMENT:
        return block_ast_builder.getClickhouseSettingBlockAst(src)


# Find nodes of the specified type (aggregate function, bool expression, conditional expression), and return a list
def findNodes(ast_root, ntype):
    if NodeType.SqlAggFunction_EXPR.value <= ntype.value < NodeType.ArithmeticExpression_EXPR.value:
        affv = AggFunctionFinderVisitor()
        ast_root.accept(affv)
        return findVisitorNodes(ntype, affv)

    elif NodeType.BooleanCompare_EXPR.value <= ntype.value < NodeType.SqlSource.value:
        befv = BooleanExpressionFinderVisitor()
        ast_root.accept(befv)
        return findVisitorNodes(ntype, befv)

    elif NodeType.CondExpression_EXPR.value <= ntype.value < NodeType.Function_EXPR.value:
        cfv = CondFinderVisitor()
        ast_root.accept(cfv)
        return findVisitorNodes(ntype, cfv)

    elif NodeType.Function_EXPR.value <= ntype.value < NodeType.BooleanCompare_EXPR.value:
        ffv = FunctionFinderVisitor()
        ast_root.accept(ffv)
        return findVisitorNodes(ntype, ffv)

    elif NodeType.SqlSource.value <= ntype.value <= NodeType.SqlFusionMergeSource.value:
        ssfv = SqlSourceFinderVisitor()
        ast_root.accept(ssfv)
        return findVisitorNodes(ntype, ssfv)

    elif ntype == NodeType.Union_SQLSTATEMENT:
        sqfv = SqlQueryFinderVisitor()
        ast_root.accept(sqfv)
        return findVisitorNodes(ntype, sqfv)

    elif NodeType.ArithmeticExpression_EXPR.value <= ntype.value <= NodeType.SubtractionExpression_EXPR.value:
        afv = ArithmeticFinderVisitor()
        ast_root.accept(afv)
        return findVisitorNodes(ntype, afv)

    elif ntype == NodeType.MapExpression_EXPR:
        befv = BaseExprFinderVisitor()
        ast_root.accept(befv)
        return findVisitorNodes(ntype, befv)

    else:
        logging.warning("current node not supported find: " + ntype.name)
        return []


# Get the dialect type of the current AST node
def getAstDialect(ast):
    query = getCurrentQueryStatement(ast)
    return query.dialect


# replace ast node
def replaceAstNode(src_node, after_node):
    replaceNode(src_node, after_node)


# Determine whether the node type is the input node type
def is_node(input_node, node_type):
    if not isinstance(input_node, SqlNode):
        return False

    if node_type == NodeType.SqlAggFunction_EXPR:
        return isAggFunction(input_node)

    if input_node.type == node_type:
        return True
    else:
        return False
