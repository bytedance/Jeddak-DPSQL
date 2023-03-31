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
QueryInterface
- Number：5001-6000
"""
from enum import Enum, unique


@unique
class QueryInterfaceErrors(Enum):
    REDERTYPE = 5001
    ADD_NOISE_ERROR = 5007
    RESULT_NULL = 5008
    QUERYINTERFACE_EXCEPTION = 5010
    CONVERT_TYPE_ERROR = 5009
