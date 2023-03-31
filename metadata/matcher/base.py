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

from metadata.database_meta import DatabaseMetadata
import copy


class MetaMatcher:
    def __init__(self, dbmeta: DatabaseMetadata):
        self.table_filter = None
        self.column_filter = None
        self.map_filter = None

        self.dbmeta = dbmeta
        self.table = None
        self.column = None

    def match_table(self, tablename):
        match_tb = self.dbmeta[tablename]
        # create new filter holding the matched table
        if len(match_tb) > 0:
            newfileter = copy.copy(self)
            newfileter.table = match_tb[0]
            return newfileter
        else:
            return None

    def match_column(self, columnname):
        column = self.table[columnname]
        if column is None:
            return None
        # create new filter holding the matched column
        newfileter = copy.copy(self)
        newfileter.column = column
        return newfileter

    def match_key_meta(self, keyname):
        key_meta = None
        if self.column.type() != "map":
            return None
        key_meta = self.column.get_key_meta(keyname)
        return key_meta
