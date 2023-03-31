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

from exception.errors import ParserError
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder
from parser.ast.builder.hive_query_ast_builder import HiveAstBuilder
from parser.ast.type.node_type import DialectType


# Obtain the corresponding builder information according to the input dialect
def get_builder(dialect):
    if dialect == DialectType.CLICKHOUSE:
        return ClickHouseAstBuilder()
    elif dialect == DialectType.HIVE:
        return HiveAstBuilder()
    else:
        return ClickHouseAstBuilder()


# Return the corresponding AST structured information according to the input sql and reader information
def get_ast(sql, reader_info):
    if reader_info == "hivereader":
        dialect_info = DialectType.HIVE
    elif reader_info in ["clickhouse"]:
        dialect_info = DialectType.CLICKHOUSE
    else:
        raise ParserError("1001", "unexpect reader: " + str(reader_info))

    builder = get_builder(dialect_info)
    ast = builder.get_query_ast(sql)
    return ast
