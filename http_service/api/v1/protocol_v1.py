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


def construct_success_task(code, task_id):
    status = {'code': code, 'taskid': task_id}
    res_json = json.dumps(status)
    return res_json


def construct_error_task(code, message):
    status = {'code': code, 'Message': message}
    res_json = json.dumps(status)
    return res_json
