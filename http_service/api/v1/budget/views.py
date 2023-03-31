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

from flask import request, Blueprint
from http_service.api.v1.budget.http_api import http_set_budget_info_interface, http_get_budget_info_interface

budget = Blueprint('budget', __name__)
# executor = ThreadPoolExecutor(20)


@budget.route('/set', methods=['POST'])
def set_budget_info():
    """ set budget info by the given params."""

    res_format = http_set_budget_info_interface(request)
    return res_format


@budget.route('/get', methods=['GET'])
def get_budget_info():
    """ visit budget info by the given params."""

    res_format = http_get_budget_info_interface(request)
    return res_format
