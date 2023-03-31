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
AnalysisError
- Number：8001-9000
"""
from enum import Enum, unique


@unique
class AnalysisErrors(Enum):
    JOIN_LEFT_ERROR = 6001
    JOIN_RIGHT_ERROR = 6002
    JOIN_CONDITION_ERROR = 6003
    NOISE_SWITCH_ERROR = 6004
    ANALYSIS_RESULT_ERROR = 6005
    SORT_SQ_ERROR = 6006
    JOIN_TYPE_UNSUPPORT = 6007
