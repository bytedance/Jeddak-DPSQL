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


from dbaccess.queryresult import QueryResult
from query_driver.context import Context
from query_driver.dpsql import DPSQLResult


def dpsqlresult_2_json(obj):
    res_dict = {
        "version": "v0.0.1",
        "context": {
            "db_info": {
                "source_sql": obj.context.get_context("source_sql"),
                "trace_id": obj.context.get_context("trace_id"),
            },
            "err": obj.context.get_context("err"),
            "method": obj.context.get_context("method"),
            "privacy": obj.context.get_context("accountant"),
            "profile": obj.context.get_context("time_perf").get_cost(),
            "sensitivity": obj.context.construct_sensitivity_info(),
            "utility": obj.context.get_context("utility_dict_list")
        },
        "query_result": {
            "col_type": list(obj.query_result.col_type),
            "result": obj.query_result.result,
        }
    }
    return res_dict


# Deserialize task execution result
def dpsqlresult_from_json(d):
    query_result = d["query_result"]
    result = query_result["result"]
    col_type = query_result["col_type"]
    query_result_obj = QueryResult(result, col_type)
    # restore context
    context_res = d["context"]
    privacy = context_res["privacy"]
    utility = context_res["utility"]
    context = Context()
    context.set_context("accountant", privacy)
    context.set_context("utility_dict_list", utility)
    context.construct_dp_info()
    dpsql_result = DPSQLResult(query_result_obj, context)
    return dpsql_result
