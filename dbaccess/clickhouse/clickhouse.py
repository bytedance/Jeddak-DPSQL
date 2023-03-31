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

from abc import ABC
from dbaccess.base import DataAccess
from clickhouse_driver import Client
from dbaccess.queryresult import QueryResult
from exception.enum.dbaccess_errors_enum import DbaccessErrors
from exception.errors import DbaccessError
from utils.singleton import Singleton


@Singleton
class ClickHouseDataAccess(DataAccess, ABC):
    """
        Support connect to ClickHouse database to execute sql, get the dataframe of result.

    """

    def __init__(self):
        pass

    def execute(self, query, dbconfig, queryconfig=None, extra=None):
        """Get QueryResult object for execute result.

                Execute sql and get the result, format result with QueryResult

                Args:
                    query: target sql.
                    dbconfig: Param for access database
                    queryconfig: Optional param for execute sql

                Returns:
                    QueryResult object contains dataframe of execute result and column type
                    example:
                    QueryResult.col_type {'col_name': col_type}
                    QueryResult.data  ((col_name1, col_name2), (data1, data2), (data3, data4))
                Raises:
                    DbaccessError: An error occurred dbaccess module process.
        """
        try:
            if dbconfig is None:
                raise DbaccessError(DbaccessErrors.READER_NULL.value, "clickhouse reader get empty dbconfig")
            database = dbconfig.get('database')
            host = dbconfig.get('host')
            user = dbconfig.get('username')
            password = dbconfig.get('password')
            port = dbconfig.get('port')
            if database is None or host is None:
                raise DbaccessError(DbaccessErrors.EMPTY_DB_HOST.value, "clickhouse reader get empty database or host")
            if user is None or len(user) == 0:
                user = 'default'
            if password is None or len(password) == 0:
                password = ''
            if port is None:
                port = "9000"
            client = Client(host=host, port=port, database=database, user=user, password=password)
            query_result = client.execute(query=query, with_column_types=True)
            # Close the current connection after querying
            client.disconnect()
            col_types, col_names, data = self._convert_to_df(query_result)
            query_result = QueryResult()
            query_result.set_type(col_types)
            query_result.set_result([tuple([col for col in col_names])] + [
                tuple(val) for val in data
            ])
        except Exception as err:
            raise DbaccessError(DbaccessErrors.ACCESS_MODULE_EXCEPTION.value, err)
        return query_result

    def _execute_ast(self, query, dbconfig, queryconfig, extra=None, pool_manager=None):
        if isinstance(query, str):
            raise DbaccessError(DbaccessErrors.EXECUTE_AST_ERROR.value, "Please pass ASTs to execute_ast.  To execute strings, use execute.")
        if hasattr(self, "serializer") and self.serializer is not None:
            query_string = self.serializer.serialize(query)
        else:
            query_string = str(query)
        return self.execute(query_string, dbconfig, queryconfig, extra, pool_manager)

    def _extract_colname_type(self, stream):
        col_names = []
        col_types = []
        for i in range(len(stream)):
            col_names.append(stream[i][0])
            col_types.append(stream[i][1])
        return col_names, col_types

    # Process raw sql interface results into a specific format
    def _convert_to_df(self, res_text):
        data, columns = res_text
        col_names, col_types = self._extract_colname_type(columns)
        return col_types, col_names, data
