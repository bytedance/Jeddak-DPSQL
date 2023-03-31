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

from enum import Enum


class AggScopeFeature(Enum):
    """
         Aggregate function level feature information.

    """
    SCOPE_1 = 30001
    SCOPE_2 = 30002
    SCOPE_3 = 30003
    SCOPE_4 = 30004
    SCOPE_5 = 30005
    SCOPE_NO_INNER = 30100
    SCOPE_NO_OUTER = 30101
    SCOPE_INNER = 30102
    SCOPE_OUTER = 30103


class AggInnerParamFeature(Enum):
    """
         Aggregation function internal parameter feature information.

    """
    MATH_FUNC = 30100

    DATABASE_TYPE_FUNC = 30200

    CONDITION_EXPR = 30300

    MATH_OPERATION = 30400
    # For the time being, it is not divided into such details, only classified into MATH OPERATION
    MATH_OPERATION_ADD = 30401
    MATH_OPERATION_SUBTRACT = 30402
    MATH_OPERATION_MULTIPLY = 30403
    MATH_OPERATION_DIVIDE = 30404
    MATH_OPERATION_MOD = 30405
    MATH_OPERATION_OPERATOR_NO_NUM = 30451

    AGG_REF = 30500

    DIRECT_NUM = 30600
    DIRECT_ALL = 30601
    DIRECT_ONE = 30602


class AggOuterOperationFeature(Enum):
    """
        Aggregation function external operation feature information.

    """
    FUNC_ALL = 31000
    FUNC_COMMON = 31001
    FUNC_MATH = 31100
    FUNC_DATABASE_TYPE = 31200
    MATH_OPERATION = 31300
    NO_OPERATION = 31400


class SqlAllFeature(Enum):
    """
        SQL overall grammatical structure feature information.

    """
    COMMON = 32000
    WITH_BLOCK = 32001
    GROUP_BY_BLOCK = 32002
    JOIN_NESTED_JOIN = 32100
    JOIN_OPERATOR_CONTAIN_SUBQUERY = 32101
    JOIN_OPERATOR_ALL_TABLE = 32102
    JOIN_OPERATOR_NUM_2 = 32103
    JOIN_OPERATOR_NUM_3 = 32104
    JOIN_OPERATOR_NUM_N = 32105
    JOIN_OPERATOR_TYPE_CROSS = 32110
