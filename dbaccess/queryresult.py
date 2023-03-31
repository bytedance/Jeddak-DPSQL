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
import logging
import prettytable as pt

from exception.enum.dbaccess_errors_enum import DbaccessErrors
from exception.errors import DbaccessError

SEQUENCE_TYPE = 0
INT_TYPE = 1
FLOAT_TYPE = 2
TEXT_TYPE = 3
UNKNOW_TYPE = -1

typeID = {
    list: SEQUENCE_TYPE,
    int: INT_TYPE,
    float: FLOAT_TYPE,
    str: TEXT_TYPE,
}


class QueryResult:
    """QueryResult Store database execution results and additional information

    Attributes:
        result: sql execution result data
        col_type: the corresponding type of the query column

    """
    def __init__(self, result=None, col_type=None):
        self.result = result
        self.col_type = col_type

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def get_meta(self):
        col_name = self.result[0]
        return dict((name, ty) for name, ty in zip(col_name, self.col_type))

    def set_type(self, col_type):
        self.col_type = col_type

    def get_type(self):
        return self.col_type

    def __str__(self):
        if self.result is None:
            return "None"
        table = pt.PrettyTable()
        table.field_names = self.result[0]
        table.add_row(self.col_type)
        for col in self.result[1:]:
            table.add_row(col)
        return str(table)

    def compare(self, other, max_rel_error, ignore_case_insensitive=False):
        other = other.get_result()
        if self.result is None and other is None:
            return True
        type1 = typeID.get(type(self.result), UNKNOW_TYPE)
        type2 = typeID.get(type(other), UNKNOW_TYPE)

        if type1 != type2:
            return False

        if type1 == SEQUENCE_TYPE:
            if (len(self.result) != len(other)) or (len(self.result[0]) != len(other[0])):
                return False
            for i in range(len(self.result)):
                for j in range(len(self.result[i])):
                    is_eq = compare_value(self.result[i][j], other[i][j], max_rel_error, ignore_case_insensitive)
                    if is_eq is False:
                        return False
            return True
        else:
            return compare_value(self, other, max_rel_error, ignore_case_insensitive)

    def __eq__(self, other):  # overload operator ==
        return self.compare(other, 0)


def compare_value(res1, res2, max_rel_error, ignore_case_insensitive=False):
    type1 = typeID.get(type(res1), UNKNOW_TYPE)
    type2 = typeID.get(type(res2), UNKNOW_TYPE)

    if type1 != type2:
        logging.error("dpaccess-internal-compare failed:")
        logging.error(res1)
        logging.error(res2)
        return False

    if (type1 == INT_TYPE) or (type1 == FLOAT_TYPE):
        if math.isnan(res1) and math.isnan(res2):
            return True
        is_close = math.isclose(res1, res2, rel_tol=max_rel_error)
        if is_close is False:
            logging.error("dpaccess-internal-compare failed:")
            logging.error(res1)
            logging.error(res2)
        return is_close
    elif type1 == TEXT_TYPE:
        if ignore_case_insensitive:
            return res1.upper() == res2.upper()
        else:
            return res1 == res2
    else:
        raise DbaccessError(DbaccessErrors.COMPARE_UNKONW_ERROR.value, "QueryResult.compare: unknow type")
