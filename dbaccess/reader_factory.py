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

from dbaccess.clickhouse.clickhouse import ClickHouseDataAccess
from dbaccess.hive.hive import HiveDataAccess
from exception.enum.dbaccess_errors_enum import DbaccessErrors
from exception.errors import DbaccessError


def reader_selector(reader_type):
    """
            Get correct reader accroading to reader type

            Args:
                reader_type: Param for select reader.
            Returns:
                Reader object
                example:
                PdpHiveDataAccess()
            Raises:
                DbaccessError: An error occurred dbaccess module process.
    """
    reader = None
    if reader_type.lower() == "clickhouse" or reader_type is None:
        reader = ClickHouseDataAccess()
    elif reader_type.lower() == "hivereader":
        reader = HiveDataAccess()
    else:
        raise DbaccessError(DbaccessErrors.LOAD_LOCAL_FILE_ERROR.value, "reader type error")
    return reader
