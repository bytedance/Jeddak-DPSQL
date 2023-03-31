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

from antlr4 import InputStream
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder, SelectBlockVisitor, \
    FromBlockVisitor, WithBlockVisitor, WhereBlockVisitor, GroupByBlockVisitor, HavingVisitor, OrderByVisitor, \
    LimitVisitor, SettingsVisitor


def getClickhouseWithBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    with_block_ast = WithBlockVisitor().visit(parser.withClause())
    return with_block_ast


def getClickhouseSelectBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    select_block_ast = SelectBlockVisitor().visit(parser.selectClause())
    return select_block_ast


def getClickhouseFromBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    from_block_ast = FromBlockVisitor().visit(parser.fromClause())
    return from_block_ast


def getClickhouseWhereBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    where_block_ast = WhereBlockVisitor().visit(parser.whereClause())
    return where_block_ast


def getClickhouseGroupByBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    groupby_block_ast = GroupByBlockVisitor().visit(parser.groupByClause())
    return groupby_block_ast


def getClickhouseHavingBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    having_block_ast = HavingVisitor().visit(parser.havingClause())
    return having_block_ast


def getClickhouseOrderByBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    orderby_block_ast = OrderByVisitor().visit(parser.orderByClause())
    return orderby_block_ast


def getClickhouseLimitBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    limit_block_ast = LimitVisitor().visit(parser.limitClause())
    return limit_block_ast


def getClickhouseLimitByBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    limitby_block_ast = LimitVisitor().visit(parser.limitByClause())
    return limitby_block_ast


def getClickhouseTeaLimitBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    tealimit_block_ast = LimitVisitor().visit(parser.tealimitClause())
    return tealimit_block_ast


def getClickhouseSettingBlockAst(str):
    builder = ClickHouseAstBuilder()
    istream = InputStream(str)
    parser = builder.get_parser(istream)
    setting_block_ast = SettingsVisitor().visit(parser.settingsClause())
    return setting_block_ast
