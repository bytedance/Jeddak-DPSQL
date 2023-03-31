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
MetaData
- Number：1001-2000
"""
from enum import Enum, unique


@unique
class MetaDataErrors(Enum):
    DBYAML_LOAD_ERROR = 1001
    DBYAML_LOAD_EXCEPTION = 1002
    DBYAML_LOAD_STR_ERROR = 1003
    CONVERTER_NOT_EMPLEMENT = 1004
    UNKNOW_COLUMN_ERROR = 1005
    DUP_COL_NAME_ERROR = 1006
    SAVE_META_STREAM_ERROR = 1007
    UNKNOW_UPDATER_ERROR = 1010
    META_MANAGER_NULL = 1012  # not used
    INIT_SYMBOL_ERROR = 1015
    VISIT_SYMBOL_ERROR = 1016
    GET_MAPKEY_ERROR = 1021
    MATCH_TABLE_EXCEPTION = 1022
    MATCH_META_ERROR = 1026
    EXTRACTOR_META_ERROR = 1027
    DB_TYPE_NONE = 1028
    HIVE_META_EXCEPTION = 1029
    MATCHERMYSQL = 1030
    META_MATCHER_NULL = 1033
    GET_DB_ID_ERROR = 1034
    VERIFY_MAP_TYPE_ERROR = 1035
    TYPE_UNSUPPORT_ERROR = 1036
    CLICKHOUSE_META_EXCEPTION = 1037
