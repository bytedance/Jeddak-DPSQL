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

class Context:
    """
        Record the current runtime environment information.

    """
    def __init__(self):
        self.context = {}

    def set_context(self, key, val):
        self.context[key] = val

    def get_context(self, key):
        if self.context.get(key):
            return self.context[key]
        else:
            return None

    def construct_sensitivity_info(self):
        sensitivities = {}
        col_name = self.get_context("source_col_names")
        sensitivity = self.get_context("sensitivities")
        if len(col_name) == len(sensitivity):
            for i in range(len(col_name)):
                sensitivities[col_name[i]] = sensitivity[i]
        return sensitivities

    # format for debug info
    def construct_debug_info(self):
        debug_info = {
            'query_info':
            {
                "source_sql": self.get_context("source_sql"),
                "rewrited_sql": self.get_context("rewrited_sql"),
                "trace_id": self.get_context("trace_id"),
            },
            'method': self.get_context("noise_method"),
            'sensitivity': self.construct_sensitivity_info(),
            'profile': self.get_context("time_perf").get_cost()
        }
        return debug_info

    # format for dp-sql info
    def construct_dp_info(self):
        dp_info = {
            'privacy': self.get_context("accountant"),
            'utility': self.get_context("utility_dict_list")
        }
        return dp_info
