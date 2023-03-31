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

import sqlalchemy
from exception.enum.utils_errors_enum import UtilsErrors
from exception.errors import UtilsError


class MysqlClient:
    def __init__(self, host, user, password=None, port=3306, db_name=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        try:
            db_url = "mysql+pymysql://%s:%s@%s:%s/%s" % (self.user, self.password, self.host, self.port, self.db_name)
            self.engine = sqlalchemy.create_engine(db_url, isolation_level="SERIALIZABLE")
        except Exception as err:
            raise UtilsError(UtilsErrors.MYSQL_CONNECT_ERROR.value, str(err))

    def get_connection(self):
        conn = self.engine.raw_connection()
        if conn is None:
            raise UtilsError(UtilsErrors.MYSQL_CONNECT_ERROR.value, "get mysql connection error")
        return conn
