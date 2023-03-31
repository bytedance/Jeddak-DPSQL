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

import time
import json
import logging


def convert_result_tojson(query_content, debug=None):
    query_result = query_content.get_query_result()
    res_dict = {}
    status = {}
    ServerInfo = {}
    query_stream = query_result.get_result()
    col_type = query_result.get_type()
    TimeZone = time.strftime('%Z', time.localtime())
    ServerInfo['TimeZone'] = TimeZone
    if len(query_stream) == 0:
        status['code'] = -1
        status['Message'] = "execute result is null"
        res_dict['status'] = status
        res_dict['ServerInfo'] = ServerInfo
        return res_dict
    meta_list = []
    # 将列名单独存储
    col_name = query_stream[0]
    for i in range(len(col_name)):
        meta_item = {'Name': col_name[i], 'Type': col_type[i]}
        meta_list.append(meta_item)

    data_item_dict = {}
    res = [([0] * (len(query_stream) - 1)) for i in range(len(query_stream[0]))]
    for j in range(len(query_stream[0])):
        for i in range(1, len(query_stream)):
            res[j][i - 1] = str(query_stream[i][j])

    for i in range(len(res)):
        data_item_dict[col_name[i]] = res[i]
    res_dict = {}
    # search successful
    status['code'] = 0
    status['Message'] = "ok"
    res_dict['status'] = status
    res_dict['ServerInfo'] = ServerInfo
    res_dict['Meta'] = meta_list
    res_dict['Data'] = data_item_dict
    # Whether to display debugging information
    if debug is True:
        res_dict['debug_info'] = query_content.get_debug_info()
    # Display key information of dp
    res_dict['dp_info'] = query_content.get_dp_info()
    res_json = json.dumps(res_dict)
    return res_json


# Unified response format for query failure
def construct_error_json(code, message):
    res_dict = {}
    status = {'code': code, 'Message': message}
    # search successful
    res_dict['status'] = status
    res_json = json.dumps(res_dict)
    return res_json


# Determine whether it is a json string
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
        logging.info("jsonfy success:", str(json_object))
    except ValueError as e:
        logging.error("json verify error:", str(e))
        return False
    return True
