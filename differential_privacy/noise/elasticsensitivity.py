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

import math


class ElasticSensitivity:
    def __init__(self):
        pass

    # 平滑敏感度
    def smooth_elastic_sensitivity(self, ji_list, epsilon, delta):
        # 距离为k的弹性敏感度
        def elastic_sensitivity_at_distance(k: int, prev_sensitivity, epsilon, delta):
            def elastic_stability(ji_list, k: int):
                # 计算两表弹性稳定度
                stability = None
                # self join
                cur_info = ji_list[0]
                if hasattr(cur_info.column1.symbol, "max_fre"):
                    mf1 = cur_info.column1.symbol.max_fre
                else:
                    mf1 = cur_info.column1.symbol.column_info.common_column_info.max_fre
                if hasattr(cur_info.column2.symbol, "max_fre"):
                    mf2 = cur_info.column2.symbol.max_fre
                else:
                    mf2 = cur_info.column2.symbol.column_info.common_column_info.max_fre
                # self join
                if cur_info.table1.table.text == cur_info.table2.table.text:
                    stability = (mf1 + k) * 1 + (mf2 + k) * 1 + 1 * 1
                else:
                    stability = max((mf1 + k) * 1, (mf2 + k) * 1)
                if len(ji_list) == 1:
                    return stability
                else:
                    for i in range(1, len(ji_list)):
                        pre_info = ji_list[i - 1]
                        cur_info = ji_list[i]
                        # 左右两结果集有交集
                        if pre_info.table2.table.text == cur_info.table2.table.text:
                            stability = stability * cur_info.column1.symbol.max_fre + cur_info.column2.symbol.max_fre * 1 + stability * 1
                        else:
                            stability = max(stability * cur_info.column1.symbol.max_fre, cur_info.column2.symbol.max_fre * 1)
                    return stability
            # 计算当前k下的弹性敏感度
            elastic_sensitivity_at_k = elastic_stability(ji_list, k)
            beta = epsilon / (2 * math.log(2 / delta))
            smooth_sensitivity = math.exp(-k * beta) * elastic_sensitivity_at_k
            if elastic_sensitivity_at_k == 0 or smooth_sensitivity < prev_sensitivity:
                return prev_sensitivity
            else:
                return elastic_sensitivity_at_distance(k + 1, smooth_sensitivity, epsilon, delta)

        return elastic_sensitivity_at_distance(0, 0, epsilon, delta)
