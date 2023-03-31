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

import copy
from sqlalchemy.testing.plugin.plugin_base import logging
from exception.enum.meradata_errors_enum import MetaDataErrors
from exception.errors import MetaDataError
from metadata import DatabaseMetadata
from metadata.matcher.base import MetaMatcher
from metadata.storage.metadata_bean_manager import get_match_table_meta, get_match_key_meta_of_hive
from metadata.converter.hive import HiveTypeConverter


class MetaMatcherForHive(MetaMatcher):
    def __init__(self, prefix, db_name):
        self.prefix = prefix
        self.db_name = db_name
        self.table_name = None
        self.type_converter = HiveTypeConverter()

    def match_table(self, tablename):
        self.table_name = tablename
        table_meta = get_match_table_meta(self.prefix, self.db_name, self.table_name)
        if table_meta:
            newfileter = copy.copy(self)
            newfileter.table = DatabaseMetadata.from_dict(table_meta).tables()[0]
            return newfileter
        else:
            raise MetaDataError(MetaDataErrors.MATCHERMYSQL.value, "MetaMatcherForHive match_table, No metadata available for " + self.table_name)

    def match_key_meta(self, keyname):
        try:
            key_meta = get_match_key_meta_of_hive(self.prefix, self.db_name, self.table_name, self.column_name, keyname)
            return key_meta
        except Exception as e:
            logging.exception("dpaccess-internal-MetaMatcherForHive query_key_meta: " + str(e))
            return None
