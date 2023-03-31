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

"""
PrivacyAccountant
- Number：4001-5000
"""
from enum import Enum, unique


@unique
class PrivacyAccountantErrors(Enum):
    ADD_ERROR = 4003
    PSM_OR_HOST_NULL = 4007
    EPSILON_NEGATIVE_ERROR = 4011
    COMPOSITION_MEMCHAINSM_ERROR = 4012
    ACCOUNTANT_SYCNOIZED_ERROR = 4021
    ACCOUNTANT_STOREGE_ERROR = 4022
