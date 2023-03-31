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

import numpy as np
import typing
from differential_privacy.accountant.accountant import PrivDataGroup


def add_raw_noise_for_join(row_in, smooth_sensitivity: typing.Iterable, epsilon, privdatas: PrivDataGroup) -> typing.Tuple[float]:
    row = [v for v in row_in]
    for idx, sen in zip(range(len(row)), smooth_sensitivity):
        if sen is not None and row[idx] is None:
            row[idx] = 0.0
    # Call all mechanisms to add noise
    out_row = list()
    for s, v in zip(smooth_sensitivity, row):
        if type(v) == str:
            out_row.append(v)
            continue
        if s is None:
            out_row.append(v)
        else:
            v = v + int(np.random.laplace(0, 2 * s / epsilon))
            out_row.append(v)
        privdatas.incrby(epsilon, delt=1e-8)  # TODO:the value of delta 1e-8 is more than budget 1e-10
    return tuple(out_row)

# if __name__ == '__main__':
#     source = 122.5
#     # 1.根据on后面的条件分别取两个表对应列的mf值
#     mf1 = 65
#     mf2 = 100
#     epsilon = 0.5
#     delta = math.pow(10, -8)
#     # 2.计算elastic_sensitivity
#     elastic_sensitivity = ElasticSensitivity()
#     # 不考虑k的弹性敏感度
#     elastic_sensitivity_regular = elastic_sensitivity.elastic_sensitivity(mf1, mf2)
#     # 3.计算平滑敏感度
#     smooth_sensitivity = elastic_sensitivity.smooth_elastic_sensitivity(elastic_sensitivity_regular, epsilon, delta)
#     print("smooth_sensitivity", smooth_sensitivity)
#     # 4.计算加噪值
#     noise = calculate_noise_via_smooth_sensitivity(smooth_sensitivity, epsilon)
#     print("result", source + noise)
