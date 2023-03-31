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


def normal_int(sensitivity, epsilon, delta):
    std = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
    return int(np.round(np.random.normal(0, std)))


def normal_float(sensitivity, epsilon, delta):
    std = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
    return np.random.normal(0, std)


def laplace_int(sensitivity, epsilon):
    return int(np.round(np.random.laplace(0, sensitivity / epsilon)))  # 取整方法是否合适


def laplace_float(sensitivity, epsilon):
    return np.random.laplace(0, sensitivity / epsilon)


def gauss_utility(sens, epsilon, delta, beta):
    alpha = 2 * sens * np.sqrt(np.log(1 / beta) * np.log(1.25 / delta)) / epsilon
    return alpha


def laplace_utility(sens, epsilon, beta):
    alpha = sens * np.log(1 / beta) / epsilon
    return alpha
