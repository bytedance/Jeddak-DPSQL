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

import uuid


def trace_id_standard(traceid, queryconfig, dbconfig):
    if traceid is None or len(traceid) == 0:
        setting = dbconfig.get('settings')
        if setting is None:
            traceid = uuid.uuid4().hex
            queryconfig["traceid"] = traceid
        else:
            traceid = setting.get('query_id')
            if traceid is None:
                traceid = uuid.uuid4().hex
                queryconfig["traceid"] = traceid
            else:
                queryconfig["traceid"] = traceid
    return traceid, queryconfig, dbconfig
