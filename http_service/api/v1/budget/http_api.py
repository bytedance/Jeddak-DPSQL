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

import json
from http_service.api.protocol_common import construct_error_json
from differential_privacy.accountant.budget import BudgetManager


def http_set_budget_info_interface(request):
    try:
        req_json = None
        req_json = request.json
        for arg in ["prefix", "db_name", "table_name", 'total_budget', 'recover_cycle', 'exhausted_strategy']:
            if req_json.get(arg) in [None, ""]:
                raise ValueError(arg + " cannot be None.")
        prefix = req_json['prefix']
        db_name = req_json['db_name']
        table_name = req_json['table_name']
        total_budget = req_json['total_budget']
        recover_cycle = req_json['recover_cycle']
        exhausted_strategy = req_json['exhausted_strategy']
        budget_manager = BudgetManager()
        budget_manager.set_budget_info(prefix, db_name, table_name, total_budget, recover_cycle, exhausted_strategy)
        res_dict = {}
        status = {'code': 200, 'Message': 'succeed'}
        res_dict['status'] = status
        res_format = json.dumps(res_dict)
    except Exception as err:
        res_format = construct_error_json(1, str(err))
    return res_format


def http_get_budget_info_interface(request):
    try:
        req_json = None
        req_json = request.json
        for arg in ["prefix", "db_name", "table_name"]:
            if req_json.get(arg) in [None, ""]:
                raise ValueError(arg + " cannot be None.")
        prefix = req_json['prefix']
        db_name = req_json['db_name']
        table_name = req_json['table_name']
        budget_manager = BudgetManager()
        res = budget_manager.get_budget_info(prefix, db_name, table_name)
        res_dict = {}
        status = {'code': 200, 'Message': 'succeed', 'data': res['data']}
        res_dict['status'] = status
        res_format = json.dumps(res_dict)
    except Exception as err:
        res_format = construct_error_json(1, str(err))
    return res_format
