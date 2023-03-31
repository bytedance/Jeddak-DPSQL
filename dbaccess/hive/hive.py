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

import logging
from abc import ABC
from dbaccess.base import DataAccess
from dbaccess.queryresult import QueryResult
from exception.enum.dbaccess_errors_enum import DbaccessErrors
from exception.errors import DbaccessError
from pyhive import hive
from utils.singleton import Singleton


@Singleton
class HiveDataAccess(DataAccess, ABC):
    """
        Support native hive access
    """

    def __init__(self):
        pass

    def execute(self, query, dbconfig, queryconfig=None, extra=None):
        try:
            if dbconfig is None:
                raise DbaccessError(DbaccessErrors.READER_NULL.value, "hive reader get empty dbconfig")
            database = dbconfig.get("database")
            username = dbconfig.get("username")
            password = dbconfig.get("password", None)
            host = dbconfig.get("host")
            port = dbconfig.get("port", 10000)
            # 连接认证方式
            if queryconfig is not None:
                auth = queryconfig.get("auth")
            if username is None or len(username) == 0:
                username = None
            if password is None or len(password) == 0:
                password = None
            # pyhive连接hive执行sql
            conn = hive.Connection(host=host, port=port, username=username, password=password, database=database,
                                   auth=auth)
            cursor = conn.cursor()
            # 执行sql
            try:
                cursor.execute(query)
            except Exception as e:
                conn.close()
                logging.exception("hive execute sql error-%s" % str(e))
                raise DbaccessError(DbaccessErrors.CONVERT_ERROR.value, "hive execute sql error-%s" % str(e))
            col_types, col_names, data = self._convert_to_df(cursor)
            # 关闭查询连接
            conn.close()
            # 查询数据
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
            raise DbaccessError(DbaccessErrors.AST_EXECUTE_ERROR.value,
                                "Please pass ASTs to execute_ast.  To execute strings, use execute.")
        if hasattr(self, "serializer") and self.serializer is not None:
            query_string = self.serializer.serialize(query)
        else:
            query_string = str(query)
        return self.execute(query_string, dbconfig, queryconfig, extra, pool_manager)

    # 获取列名类型
    def _convert_to_df(self, cursor):
        # 获取列名和列类型
        content = cursor.description
        col_names, col_types = self._extract_colname_type(content)
        res_data = cursor.fetchall()
        return col_types, col_names, res_data

    # 提取列名和列类型
    def _extract_colname_type(self, content):
        col_names = []
        col_types = []
        for i in range(len(content)):
            item = content[i]
            col_arr = item[0].split(".")
            col_name = col_arr[-1]
            col_names.append(col_name)
            col_type = item[1].replace("_TYPE", "")
            col_types.append(col_type)
        return col_names, col_types
