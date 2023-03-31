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

from parser.ast.expr.agg_function_expr import SqlAggFunction


def is_contain_join(struct_info):
    if len(struct_info.struct_join_info.join_infos) >= 1:
        return True
    else:
        return False


# Determine whether there is an aggregate function
def get_agg_items(symbols):
    pass


# Determine whether there is an aggregation operation in the outermost layer
def is_contain_aggfunc(symblos):
    tag = False
    for item in symblos:
        if isinstance(item[1], SqlAggFunction) or (
                hasattr(item[1], "symbol") and isinstance(item[1].symbol, SqlAggFunction)):
            tag = True
            break
    return tag
