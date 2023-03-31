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

"""
Dbaccess
- Number：3001-4000
"""
from enum import Enum, unique


@unique
class DbaccessErrors(Enum):
    EXECUTE_SQL_ERROR = 3001
    RESPONSE_ERROR = 3002
    EXECUTE_AST_ERROR = 3003
    READER_NULL = 3004
    EMPTY_DB_HOST = 3005
    AST_EXECUTE_ERROR = 3006
    AST_ERROR = 3007
    COMPARE_UNKONW_ERROR = 3008
    ACCESS_MODULE_EXCEPTION = 3011
    FILE_LOCAL_ERROR = 3012
    LOAD_LOCAL_FILE_ERROR = 3013
    CONVERT_ERROR = 3015
