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

from exception.enum.meradata_errors_enum import MetaDataErrors
from metadata.matcher.clickhouse import MetaMatcherForClickhouse
from metadata.matcher.base import MetaMatcher
from exception.errors import MetaDataError
import logging
from metadata.matcher.hive import MetaMatcherForHive


def get_metamatcher(sql: str, dbconfig: dict, traceid: str) -> MetaMatcher:
    dbname = dbconfig["database"]
    reader_type = dbconfig.get('reader')
    if reader_type.lower() == "clickhouse":
        host = dbconfig.get('host')
        meta_matcher = MetaMatcherForClickhouse(host, dbname)
    elif reader_type.lower() == "hivereader":
        host = dbconfig.get('host')
        meta_matcher = MetaMatcherForHive(host, dbname)
    else:
        logging.error("dpaccess-internal-get_metamatcher: " + traceid + "No available metadata matcher.")
        raise MetaDataError(MetaDataErrors.META_MATCHER_NULL.value, "No available metadata matcher.")
    return meta_matcher
