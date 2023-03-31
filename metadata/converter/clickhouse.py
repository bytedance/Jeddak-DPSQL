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

import logging
from .base import BaseTypeConverter
import re

# TODO: add all clickhouse datatypes
TYPE_DICT = {
    # clickhouse
    "Int8": "int",
    "Int16": "int",
    "Int32": "int",
    "Int64": "int",
    "Int128": "int",
    "Int256": "int",
    "UInt8": "int",
    "UInt16": "int",
    "UInt32": "int",
    "UInt64": "int",
    "UInt128": "int",
    "UInt256": "int",
    "Float32": "float",
    "Float64": "float",
    "String": "string",
    "Date": "datetime",
    "DateTime": "datetime",
    "DateTime64": "datetime",
    "UUID": "string",
    # ""
}


# TODO: add all clickhouse functions
# TODO: handle multiple dialects
FUNCTYPE_DICT = {
    # clickhouse
    # 1.Type Conversion Functions
    "toInt8": "Int8",
    "toInt16": "Int16",
    "toInt32": "Int32",
    "toInt64": "Int64",
    "toInt128": "Int128",
    "toInt256": "Int256",
    "reinterpretAsInt8": "Int8",
    "reinterpretAsInt16": "Int16",
    "reinterpretAsInt32": "Int32",
    "reinterpretAsInt64": "Int64",
    "toUInt8": "UInt8",
    "toUInt16": "UInt16",
    "toUInt32": "UInt32",
    "toUInt64": "UInt64",
    "toUInt128": "UInt128",
    "toUInt256": "UInt256",
    "reinterpretAsUInt8": "UInt8",
    "reinterpretAsUInt16": "UInt16",
    "reinterpretAsUInt32": "UInt32",
    "reinterpretAsUInt64": "UInt64",
    "toInt8OrZero": "Int8",
    "toInt16OrZero": "Int16",
    "toInt32OrZero": "Int32",
    "toInt64OrZero": "Int64",
    "toInt128OrZero": "Int128",
    "toInt256OrZero": "Int256",
    "toInt8OrNull": "Int8",
    "toInt16OrNull": "Int16",
    "toInt32OrNull": "Int32",
    "toInt64OrNull": "Int64",
    "toInt128OrNull": "Int128",
    "toInt256OrNull": "Int256",
    "toFloat32": "Float32",
    "toFloat64": "Float64",
    "toFloat32OrZero": "Float32",
    "toFloat64OrZero": "Float64",
    "toFloat32OrNull": "Float32",
    "toFloat64OrNull": "Float64",
    "reinterpretAsFloat32": "Float32",
    "reinterpretAsFloat64": "Float64",
    "toString": "String",
    "toFixedString": "String",
    "toStringCutToZero": "String",
    "reinterpretAsString": "String",
    "reinterpretAsFixedString": "String",
    "toDate": "Date",
    "toDateOrZero": "Date",
    "toDateOrNull": "Date",
    "reinterpretAsDate": "Date",
    "reinterpretAsDateTime": "DateTime",
    "toDateTime": "DateTime",
    "toDateTime64": "DateTime64",
    # 2.Mathematical
    "pow": "Float64",
    "power": "Float64",
    # 3.Aggregate Functions
    "count": "UInt64",
    "avg": "Float64",
    "varPop": "Float64",
    "stddevPop": "Float64",
    # 4.Arithmetic
    "/": "Float64",
    "%": "UInt64",
    "divide": "Float64",
    "max2": "Float64",
    # 5.logic function
    "or": "UInt8",
    "and": "UInt8",
    "not": "UInt8",
    "xor": "UInt8",
    # 6.comparison function
    "equals": "UInt8",
    "notEquals": "UInt8",
    "less": "UInt8",
    "greater": "UInt8",
    "lessOrEquals": "UInt8",
    "greaterOrEquals": "UInt8",
    # Functions for Working with Strings
    "empty": "UInt8",
    "notEmpty": "UInt8",
    # FIXME: need refactoring
    "transform": "String",
    "intDiv": "String",
    "intDivOrZero": "String",
    "moduloOrZero": "String",
    "negate": "String",
    "abs": "String",
    "gcd": "String",
    "lcm": "String",
    "reinterpret": "String",
    "CAST": "String",



}


LITRAL_TYPE_DICT = {
    # clickhouse
    "string": "String",
    "float": "Float64",
    "int": "Int32",
    "boolean": "UInt8",
}


OP_TYPE_RANKING = {
    "UInt8": 0,
    "UInt16": 1,
    "UInt32": 2,
    "UInt64": 3,
    "UInt128": 4,
    "UInt256": 5,
    "Int8": 10,
    "Int16": 11,
    "Int32": 12,
    "Int64": 13,
    "Int128": 14,
    "Int256": 15,
    "Float32": 22,
    "Float64": 23,
}

OP_TYPE_RANKING_INVERSE = {
    0: "UInt8",
    1: "UInt16",
    2: "UInt32",
    3: "UInt64",
    4: "UInt128",
    5: "UInt256",
    10: "Int8",
    11: "Int16",
    12: "Int32",
    13: "Int64",
    14: "Int128",
    15: "Int256",
    20: "Float32",
    21: "Float32",
    22: "Float32",
    23: "Float64",
    24: "Float64",
    25: "Float64",
}


class ClickhouseTypeConverter(BaseTypeConverter):
    ENGINE = "clickhouse"

    def dbtype_to_type(self, dbtype):
        try:
            Nullable_flag = re.match(r'Nullable[(](.*)[)]', dbtype)
            if Nullable_flag:
                dbtype = Nullable_flag.group(1)
            if dbtype.lower().startswith("array"):
                return "array"
            if dbtype.lower().startswith("map"):
                return "map"
            if dbtype.lower().startswith("decimal"):
                return "float"
            return TYPE_DICT[dbtype]
        except KeyError:
            raise TypeError("dbtype_to_type Unsupported type %s" % (dbtype))

    def function_dbtype(self, funcname):
        try:
            return FUNCTYPE_DICT[funcname]
        except KeyError:
            raise TypeError("function_dbtype Unsupported function %s" % (funcname))

    def function_type(self, funcname):
        try:
            dbtype = FUNCTYPE_DICT[funcname]
        except KeyError:
            raise TypeError("function_type Unsupported function %s" % (funcname))
        return self.dbtype_to_type(dbtype)

    # TODO: set type width according to value

    def litral_dbtype(self, tp, value):
        try:
            return LITRAL_TYPE_DICT[tp]
        except KeyError:
            raise TypeError("litral_dbtype Unsupported litral type %s" % (tp))

    # FIXME: handle different type more properly, consider type width

    def op_dbtype(self, op, ltn, rtn):
        # fixed return type
        if op == "/" or op == "%":
            return self.function_dbtype(op)
        # for "*", "+", "-"
        l_ranking = OP_TYPE_RANKING.get(ltn, -1)
        r_ranking = OP_TYPE_RANKING.get(rtn, -1)
        if l_ranking == -1 or r_ranking == -1:
            logging.error("dpaccess-internal-Unsupported type %s %s" % (ltn, rtn))
            raise TypeError("op_dbtype Unsupported type %s %s" % (ltn, rtn))
        # determine type
        l_typ = l_ranking // 10
        r_typ = r_ranking // 10
        typ = l_typ if l_typ > r_typ else r_typ
        # determine width
        l_width = l_ranking % 10
        r_width = r_ranking % 10
        width = l_width if l_width > r_width else r_width

        full_typ = typ * 10 + width

        return OP_TYPE_RANKING_INVERSE.get(full_typ, None)
