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

from parser.ast.expr.cond_expr import CoalesceFuncExpression
from parser.ast.expr.function_expr import MathFunction
from parser.ast.expr.hive_cond_expr import NvlFuncExpression, NullIfFuncExpression, AssertTrueFuncExpression
from parser.ast.type.sql_type import HiveSqlNumberType

HIVE_MATH_FUNCTION_LIST = [
    "ABS",
    "ACOS",
    "ASIN",
    "ATAN",
    "BROUND",
    "CBRT",
    "CEIL",
    "CEILING",
    "COS",
    "DEGREES",
    "E",
    "EXP",
    "FACTORIAL",
    "FLOOR",
    "LN",
    "LOG2",
    "LOG10",
    "PI",
    "POW",
    "POWER",
    "RADIANS",
    "RAND",
    "ROUND",
    "SIN",
    "SQRT",
    "TAN",
    "WIDTH_BUCKET"
]

# The return value of all mathematical functions is DOUBLE by default, and the special return value of the mathematical function is single column
HIVE_MATH_TYPE_MAPPING = {
    "CEIL": HiveSqlNumberType.BIGINT,
    "CEILING": HiveSqlNumberType.BIGINT,
    "FACTORIAL": HiveSqlNumberType.BIGINT,
    "FLOOR": HiveSqlNumberType.BIGINT,
    "WIDTH_BUCKET": HiveSqlNumberType.INT,
    "DEFAULT": HiveSqlNumberType.DOUBLE
}

HIVE_COND_FUNCTION_LIST = [
    "NVL",
    "COALESCE",
    "NULLIF",
    "ASSERT_TRUE"
]


def get_math_func_type(func_name):
    for key, value in HIVE_MATH_TYPE_MAPPING:
        if str(func_name).upper() == key:
            return value
    return HIVE_MATH_TYPE_MAPPING["DEFAULT"]


def hive_switch_cond_func(func_name, arg_list):
    if func_name == "NVL":
        nvl_func = NvlFuncExpression()
        value = arg_list[0]
        default_value = arg_list[1]
        nvl_func.value = value
        nvl_func.default_value = default_value
        return nvl_func
    elif func_name == "COALESCE":
        cfe = CoalesceFuncExpression()
        for arg in arg_list:
            cfe.args.append(arg)
        return cfe
    elif func_name == "NULLIF":
        nif = NullIfFuncExpression()
        nif.first_arg = arg_list[0]
        nif.second_arg = arg_list[1]
        return nif
    elif func_name == "ASSERT_TRUE":
        ae = AssertTrueFuncExpression()
        ae.condition = arg_list[0]
        return ae
    else:
        return None


def hive_switch_func(func_name, column_list, arg_list, distinct_flag):
    if str(func_name).upper() in HIVE_MATH_FUNCTION_LIST:
        mf = MathFunction(func_name)
        if arg_list is not None:
            for arg in arg_list:
                mf.args.append(arg)
        mf_type = get_math_func_type(func_name)
        mf.db_type = mf_type
        return mf
    elif str(func_name).upper() in HIVE_COND_FUNCTION_LIST:
        return hive_switch_cond_func(str(func_name).upper(), arg_list)
    else:
        return None
