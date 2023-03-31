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
from parser.ast.base import ColumnInfo, MapExpressionInfo, SqlNode
from parser.ast.type.node_type import NodeType, JoinKind
from parser.ast.visitor.base_ast_visitor import BaseAstVisitor
import copy


class InitSymbolLoadingVisitor(BaseAstVisitor):
    def __init__(self):
        pass

    def visitSelectBlockStatement(self, node):
        node.m_symbols = []

    def visitTable(self, node):
        node.columns.clear()


class SQSymbolLoadingVisitor(BaseAstVisitor):
    def __init__(self, sq):
        self.sq = sq

    def visitSelectItem(self, node):
        def is_in_m_symbols(node_name, m_symbols):
            for name, symbol in m_symbols:
                if node_name == name:
                    return True
            return False

        current_query = ast_utils.getCurrentQueryStatement(node)
        current_select = current_query.select_block

        ssisl = SQSelectItemSymbolLoadingVisitor(self.sq, current_select)
        node.expr.accept(ssisl)
        if node.alias is not None:
            node.alias.symbol = node.expr
            if is_in_m_symbols(str(node.alias), current_select.m_symbols) is False:
                current_select.m_symbols.append((str(node.alias), node.expr))
        else:
            if is_in_m_symbols(str(node), current_select.m_symbols) is False:
                if node.expr.type == NodeType.Identifier_EXPR:
                    current_select.m_symbols.append((str(node), node.expr))

    def visitJoinConstraintExpr(self, node):
        # current_query = AstUtils.getCurrentQueryStatement(node)
        sjv = SQJoinSymbolLoadingVisitor(self.sq)
        for condition in node.conditions:
            condition.accept(sjv)


class SQJoinSymbolLoadingVisitor(BaseAstVisitor):
    def __init__(self, sq):
        self.sq = sq
        self.sq_tables = self.sq.virtual_tables

    def visitIdentifier(self, node):
        column_infos = str(node).split('.')
        if len(column_infos) == 2:
            table_name = column_infos[0]
            column_name = column_infos[1]
        elif len(column_infos) == 3:
            table_name = column_infos[1]
            column_name = column_infos[2]
        else:
            table_name = None
            column_name = str(node)

        if table_name is not None:
            for sq_table in self.sq_tables:
                if str(table_name) == sq_table.name:
                    node_symbol_info = self._find_column_info(column_name, sq_table)
                    if node_symbol_info is not None:
                        node.symbol = node_symbol_info
                        return
        else:
            for sq_table in self.sq_tables:
                node_symbol_info = self._find_column_info(column_name, sq_table)
                if node_symbol_info is not None:
                    node.symbol = node_symbol_info
                    return

    def _find_column_info(self, column_name, sq_table):
        for column in sq_table.columns:
            if str(column) == str(column_name):
                return column

        return None

class SymbolLoadingVisitor(BaseAstVisitor):

    def __init__(self, metamatcher=None):
        self.meta_matcher = metamatcher
        self.m_symbols = {}  # column's symbols
        # If there is a table, the list size is 1
        self.m_tables_columns = []
        self.column_matcher = None

    def visitTable(self, node):
        # need load table column, depend on metadata
        # print("haha, find table : " + AstUtils.tosql(node, DialectType.CLICKHOUSE))
        if self.meta_matcher is None:
            return
        else:
            table_name = str(node).split('.')[1] if len(str(node).split('.')) > 1 else str(node)
            self.column_matcher = self.meta_matcher.match_table(table_name.strip("`"))
            table = self.column_matcher.table
            tc = table.m_columns
            for name in tc.keys():
                if tc[name].type() == "map":
                    ci = MapExpressionInfo()
                    ci.name = name
                    ci.columnValue_type = tc[name].type()
                    ci.columnValue_dbtype = tc[name]._dbtype
                    ci.bounded = tc[name].bounded
                    ci.is_key = tc[name].is_key
                    ci.key_dbtype = tc[name].key_dbtype
                    ci.key_metas = tc[name].key_metas
                    ci.key_metas_event_name_dict = tc[name].key_metas_event_name_dict
                    ci.key_type = tc[name].key_type
                    ci.max_fre = tc[name].max_fre
                    ci.value_dbtype = tc[name].value_dbtype
                    ci.value_type = tc[name].value_type
                    ci.table_name = table.name
                else:
                    ci = ColumnInfo()
                    ci.name = name
                    ci.columnValue_type = tc[name].type()
                    ci.columnValue_dbtype = tc[name]._dbtype
                    ci.is_key = tc[name].is_key
                    ci.bounded = tc[name].bounded
                    ci.minval = tc[name].minval if tc[name].type() in ["int", "float"] else None
                    ci.maxval = tc[name].maxval if tc[name].type() in ["int", "float"] else None
                    ci.max_fre = tc[name].max_fre if tc[name].type() in ["int", "float", "string"] else None
                    ci.clipping_flag = tc[name].clipping_flag if tc[name].type() in ["int", "float"] else None
                    ci.table_name = table.name

                node.columns.append(ci)

    def visitSelectItem(self, node):
        def is_in_m_symbols(node_name, m_symbols):
            for name, symbol in m_symbols:
                if node_name == name:
                    return True
            return False

        # print("haha, find select item : " + AstUtils.tosql(node, DialectType.CLICKHOUSE))
        current_query = ast_utils.getCurrentQueryStatement(node)
        current_with = current_query.with_block
        current_select = current_query.select_block
        current_source = current_query.source_block

        sisl = SelectItemSymbolLoadingVisitor(current_with, current_select, current_source)
        node.expr.accept(sisl)
        if node.alias is not None:
            node.alias.symbol = node.expr
            if is_in_m_symbols(str(node.alias), current_select.m_symbols) is False:
                current_select.m_symbols.append((str(node.alias), node.expr))
        else:
            if is_in_m_symbols(str(node), current_select.m_symbols) is False:
                if node.expr.type == NodeType.Identifier_EXPR:
                    current_select.m_symbols.append((str(node), node.expr.symbol))
                else:
                    current_select.m_symbols.append((str(node), node.expr))

    def visitMapExpression(self, node):
        # print("haha, find mapExpression: " + AstUtils.tosql(node, DialectType.CLICKHOUSE))

        current_query = ast_utils.getCurrentQueryStatement(node)
        current_with = current_query.with_block
        current_select = current_query.select_block
        current_source = current_query.source_block

        current_with_symbols = ast_utils.getAllSymbolsFromWithBlock(current_with)
        current_select_symbols = current_select.m_symbols
        current_source_symbols = ast_utils.getAllSymbolsFromSourceBlock(current_source)

        # wait to check
        for name, symbol in current_select_symbols:
            if str(name) == str(node.map_name):
                newfilter = copy.copy(self.meta_matcher)
                # newfilter.column = symbol
                newfilter.column_name = name
                key = str(node.map_key)
                key = key[1:-1]
                key_meta = newfilter.match_key_meta(key)
                node.map_info = copy.copy(symbol)
                node.map_info.key_meta = key_meta
                if key_meta is not None:
                    node.map_info.maxval = key_meta.get("upper") or 0
                    node.map_info.minval = key_meta.get("lower") or 0
        # for name, symbol in current_with_symbols:
        #     newfilter = copy.copy(self.meta_matcher)
        #     newfilter.column = symbol
        #     key = str(node.map_key)
        #     key = key[1:-1]
        #     key_meta = newfilter.match_key_meta(key)
        # #**********************
        for name, symbol in current_source_symbols:
            if str(name) == str(node.map_name):
                newfilter = copy.copy(self.meta_matcher)
                # newfilter.column = symbol
                newfilter.column_name = name
                key = str(node.map_key)
                key = key[1:-1]
                key_meta = newfilter.match_key_meta(key)
                node.map_info = copy.copy(symbol)
                node.map_info.key_meta = key_meta
                if key_meta is not None:
                    node.map_info.maxval = key_meta.get("upper") or 0
                    node.map_info.minval = key_meta.get("lower") or 0

    def visitWithBlockStatement(self, node):
        pass
        # print("haha, find with block statement")

    def visitSqlTableJoinSource(self, node):
        current_query = ast_utils.getCurrentQueryStatement(node)
        current_with = current_query.with_block
        current_select = current_query.select_block
        current_source = current_query.source_block

        sisl = SelectItemSymbolLoadingVisitor(current_with, current_select, current_source)
        if node.join_type.kind != JoinKind.Cross:
            node.join_condition.accept(sisl)


class SQSelectItemSymbolLoadingVisitor(BaseAstVisitor):
    def __init__(self, sq, selectb):
        self.select_symbols = selectb.m_symbols

    def visitIdentifier(self, node):

        for name, symbol in self.select_symbols:
            if str(name) == str(node):
                node.symbol = symbol
                return
        src_exprs = node.state.src_expr
        if len(src_exprs) > 0:
            node.symbol = src_exprs[0]


class SelectItemSymbolLoadingVisitor(BaseAstVisitor):

    def __init__(self, withb, selectb, sourceb):
        self.withb = withb
        self.selectb = selectb
        self.sourceb = sourceb
        self.select_symbols = selectb.m_symbols
        self.with_symbols = ast_utils.getAllSymbolsFromWithBlock(withb)
        self.source_symbols = ast_utils.getAllSymbolsFromSourceBlock(sourceb)

    def visitIdentifier(self, node):
        # print("haha, find identifier:", str(node))
        node_text = node.text
        if "." in node_text:
            text_split = node_text.split(".")
            if len(text_split) != 2:
                raise
            table_name = text_split[0]
            node_name = text_split[-1]
            for name, symbol in self.select_symbols:
                if isinstance(symbol, SqlNode):
                    symbol_table_alias = ast_utils.getCurrentQueryAlias(symbol)
                    if symbol_table_alias is None:
                        continue
                else:
                    symbol_table_alias = symbol.table_name

                if str(name) == node_name and str(symbol_table_alias) == table_name:
                    node.symbol = symbol
                    return
            for name, symbol in self.with_symbols:
                if isinstance(symbol, SqlNode):
                    symbol_table_alias = ast_utils.getCurrentQueryAlias(symbol)
                    if symbol_table_alias is None:
                        continue
                else:
                    symbol_table_alias = symbol.table_name

                if str(name) == node_name and str(symbol_table_alias) == table_name:
                    node.symbol = symbol
                    return
            for name, symbol in self.source_symbols:
                if isinstance(symbol, SqlNode):
                    symbol_table_alias = ast_utils.getCurrentQueryAlias(symbol)
                    if symbol_table_alias is None:
                        continue
                else:
                    symbol_table_alias = symbol.table_name
                if str(name) == node_name and str(symbol_table_alias) == table_name:
                    node.symbol = symbol
                    return

        for name, symbol in self.select_symbols:
            if str(name) == str(node):
                node.symbol = symbol
                return
        for name, symbol in self.with_symbols:
            if str(name) == str(node):
                node.symbol = symbol
                return
        for name, symbol in self.source_symbols:
            if str(name) == str(node):
                node.symbol = symbol
                return
