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
from dbaccess.reader_factory import reader_selector
from exception.enum.dbaccess_errors_enum import DbaccessErrors
from exception.errors import DbaccessError


class DbAccess:
    """
        DataAccess object for access database and execute sql, connect query driver to database engine.

        Attributes:
            dbconfig: Param for connect to database
    """
    def __init__(self, dbconfig=None):
        self.db_type = dbconfig.get('reader')
        if self.db_type is None:
            self.db_type = "clickhouse"
        self.reader = reader_selector(self.db_type)
        self.host = dbconfig.get('host')

    def execute(self, query, dbconfig, queryconfig, extra=None):
        return self.reader.execute(query=query, dbconfig=dbconfig, queryconfig=queryconfig, extra=extra)

    def execute_ast(self, query, dbconfig, queryconfig, extra=None):
        if isinstance(query, str):
            raise DbaccessError(DbaccessErrors.AST_ERROR.value, "Please pass ASTs to execute_ast.  To execute strings, use execute.")
        if hasattr(self, "serializer") and self.serializer is not None:
            query_string = self.serializer.serialize(query)
        else:
            query_string = str(query)
        return self.execute(query_string, dbconfig, queryconfig, extra)

    def get_reader(self):
        return self.reader
