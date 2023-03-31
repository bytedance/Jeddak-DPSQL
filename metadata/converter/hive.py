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
from metadata.converter.base import BaseTypeConverter

TYPE_DICT = {
    "tinyint": "int",
    "smallint": "int",
    "int": "int",
    "integer": "int",
    "bigint": "int",
    "boolean": "bool",
    "float": "float",
    "double": "float",
    "decimal": "float",
    "string": "string",
    "varchar": "string",
    "char": "string",
    "timestamp": "datetime",
    "date": "datetime"
}

#  mapping between operator/function and result type
FUNCTYPE_DICT = {
    # Relational Operators
    "=": "boolean",
    "==": "boolean",
    "<==>": "boolean",
    "is null": "boolean",
    "is not null": "boolean",
    # Arithmetic Operators
    "/": "double",
    "div": "integer",
    # Logical Operators
    "in": "boolean",
    "not in": "boolean",
    "exists": "boolean",
    "not exists": "boolean",
    # Mathematical Functions
    "round": "double",
    "floor": "bigint",
    "ceil": "bigint",
    "ceiling": "bigint",
    "rand": "double",
    "exp": "double",
    "ln": "double",
    "log10": "double",
    "log2": "double",
    "log": "double",
    "pow": "double",
    "power": "double",
    "sqrt": "double",
    "bin": "string",
    "hex": "string",
    "abs": "double",
    "e": "double",
    "pi": "double",
    "factorial": "bigint",
    # Date Fcuntion
    "from_unixtime": "string",
    "unix_timestamp": "bigint",
    "year": "int",
    "quarter": "int",
    "month": "int",
    "day": "int",
    "hour": "int",
    "minute": "int",
    "second": "int",
    "weekofyear": "int",
    "extract": "int",
    "datediff": "int",
    "from_utc_timestamp": "timestamp",
    "to_utc_timestamp": "timestamp",
    "current_date": "date",
    "current_timestamp": "timestamp",
    "add_months": "string",
    "last_day": "string",
    "next_day": "string",
    "trunc": "string",
    "months_between": "double",
    "date_format": "string",
    # Conditional Functions
    "isnull": "boolean",
    "isnotnull": "boolean",
    # Aggregate Functions
    "count": "bigint",
    "sum": "double",
    "avg": "double",
    "min": "double",
    "max": "double",
    "variance": "double",
    "var_pop": "double",
    "var_samp": "double",
    "stddev_pop": "double",
    "stddev_samp": "double",
    "covar_pop": "double",
    "covar_samp": "double",
    "corr": "double",
    "percentile": "double",
    "percentile_approx": "double",
    "regr_avgx": "double",
    "regr_avgy": "double",
    "regr_count": "double",
    "regr_intercept": "double",
    "regr_r2": "double",
    "regr_slope": "double",
    "regr_sxx": "double",
    "regr_sxy": "double",
    "regr_syy": "double",
}

LITRAL_TYPE_DICT = {
    "string": "string",
    "float": "float",
    "int": "int",
    "boolean": "boolean"
}

OP_TYPE_RANKING = {
    "tinyint": 0,
    "smallint": 1,
    "int": 2,
    "integer": 3,
    "bigint": 4,
    "float": 5,
    "double": 6
}


class HiveTypeConverter(BaseTypeConverter):
    ENGINE = "hive"

    def dbtype_to_type(self, dbtype):
        try:
            if dbtype.lower().startswith("array"):
                return "array"
            if dbtype.lower().startswith("map"):
                return "map"
            return TYPE_DICT[dbtype.lower()]
        except KeyError:
            raise TypeError("HiveTypeConverter-dbtype_to_type Unsupported type %s" % (dbtype))

    def function_dbtype(self, funcname):
        try:
            return FUNCTYPE_DICT[funcname]
        except KeyError:
            raise TypeError("HiveTypeConverter-function_dbtype Unsupported function %s" % (funcname))

    def function_type(self, funcname):
        try:
            dbtype = FUNCTYPE_DICT[funcname]
        except KeyError:
            raise TypeError("HiveTypeConverter-function_type Unsupported function %s" % (funcname))
        return self.dbtype_to_type(dbtype)

    def litral_dbtype(self, tp, value):
        try:
            return LITRAL_TYPE_DICT[tp]
        except KeyError:
            raise TypeError("HiveTypeConverter-litral_dbtype Unsupported litral type %s" % (tp))

    def op_dbtype(self, op, ltn, rtn):
        if op == "/" or op == "div":
            return self.function_dbtype(op)
        # for "+", "-", "*", "%"
        l_ranking = OP_TYPE_RANKING.get(ltn, -1)
        r_ranking = OP_TYPE_RANKING.get(rtn, -1)
        if l_ranking == -1 or r_ranking == -1:
            logging.error("dpaccess-internal-HiveTypeConverter-Unsupported type %s %s" % (ltn, rtn))
            raise TypeError("HiveTypeConverter-op_dbtype Unsupported type %s %s" % (ltn, rtn))
        return ltn if l_ranking > r_ranking else rtn
