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

import operator
import numpy as np
from parser.ast.base import SqlExpr
from parser.ast.type.node_type import OperatorType, NodeType, LogicalInType, LogicalLikeType
from datetime import datetime, date

ops = {
    OperatorType.LT: operator.gt,
    OperatorType.GT: operator.lt,
    OperatorType.LE: operator.ge,
    OperatorType.GE: operator.le,
    OperatorType.EQ_DOUBLE: operator.eq,
    OperatorType.NOT_EQ_1: operator.ne,
    OperatorType.NOT_EQ_2: operator.ne,
    NodeType.LogicalAnd_EXPR: np.logical_and,
    NodeType.LogicalConcat_EXPR: np.logical_or,
}


class BooleanCompare(SqlExpr):
    def __init__(self):
        super(BooleanCompare, self).__init__()
        self.type = NodeType.BooleanCompare_EXPR

    def dbtype(self, converter):
        return "boolean"

    def type(self):
        return "boolean"


class BaseBooleanCompare(BooleanCompare):
    def __init__(self):
        super(BaseBooleanCompare, self).__init__()
        self.left = None
        self.right = None

    def sensitivity(self):
        return 1

    def coerce_string(self, val, typed_val):
        # SQL-92 rules for casting types in comparison
        if isinstance(typed_val, bool):
            return parse_bool(val)
        elif isinstance(typed_val, int):
            try:
                v = int(val)
            except ValueError:
                v = float(val)
            return v
        elif isinstance(typed_val, float):
            return float(val)
        elif isinstance(typed_val, datetime):
            return datetime.fromisoformat(val)
        elif isinstance(typed_val, date):
            return date.fromisoformat(val)
        else:
            return val

    def evaluate(self, bindings):
        left = self.left.evaluate(bindings)
        right = self.right.evaluate(bindings)
        if type(left) != type(right):
            if isinstance(left, str):
                left = self.coerce_string(left, right)
            elif isinstance(right, str):
                right = self.coerce_string(right, left)
        try:
            res = bool(ops[self.type](left, right))
        except Exception:
            raise ValueError(
                "We don't know how to compare {0} {1} {2} of mismatched types {3} and {4}".format(
                    left, self.type, right, str(type(left)), str(type(right))
                )
            )
        return parse_bool(res)


# Assignment or Judgment
# a = b
class BinaryEqual(BaseBooleanCompare):
    def __init__(self, left, right):
        super(BinaryEqual, self).__init__()
        self.type = NodeType.BinaryEqual_EXPR
        self.left = left
        self.right = right
        self.operator = OperatorType.EQ_SINGLE

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " = " + str(self.right)

    def clone(self):
        bc = BinaryEqual(None, None)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a == b
# a != b
# a <> b
class LogicalEqual(BaseBooleanCompare):
    def __init__(self, left, right, operator):
        super(LogicalEqual, self).__init__()
        self.type = NodeType.LogicalEqual_EXPR
        self.left = left
        self.right = right
        self.operator = operator

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        if self.operator == OperatorType.EQ_DOUBLE:
            operator_info = " == "
        elif self.operator == OperatorType.HIVE_EQ_NS:
            operator_info = " <=> "
        elif self.operator == OperatorType.NOT_EQ_1:
            operator_info = " != "
        else:
            operator_info = " <> "
        return str(self.left) + operator_info + str(self.right)

    def clone(self):
        bc = LogicalEqual(None, None, self.operator)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# NOT a
class LogicalNot(BooleanCompare):
    def __init__(self, expr):
        super(LogicalNot, self).__init__()
        self.type = NodeType.LogicalNot_EXPR
        self.expr = expr

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return " NOT " + str(self.expr)

    def clone(self):
        bc = LogicalNot(None)
        if hasattr(self.expr, "clone"):
            bc.expr = self.expr.clone()
        else:
            bc.expr = self.expr

        return bc

    def type(self):
        return "boolean"

    # FIXME
    def dbtype(self, converter):
        return "boolean"

    def sensitivity(self):
        return 1

    def evaluate(self, bindings):
        val = self.expr.evaluate(bindings)
        return not parse_bool(val)


# [NOT] EXISTS (subquery)
class ExistsQuery(BooleanCompare):
    def __init__(self, not_flag, query):
        super(ExistsQuery, self).__init__()
        self.type = NodeType.LogicalExistsQuery_EXPR
        self.not_flag = not_flag
        self.query = query

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.query.accept(visitor)

    def __str__(self):
        if self.not_flag is True:
            return " NOT EXISTS (" + str(self.query) + ")"
        else:
            return " EXISTS (" + str(self.query) + ")"

    def clone(self):
        eq = ExistsQuery(None, None)
        eq.not_flag = self.not_flag
        if hasattr(self.query, "clone"):
            eq.query = self.query.clone()
        else:
            eq.query = self.query

        return eq

    def type(self):
        return "boolean"

    # FIXME
    def dbtype(self, converter):
        return "boolean"

    def sensitivity(self):
        return 1

    def evaluate(self, bindings):
        val = self.query.evaluate(bindings)
        return not parse_bool(val)


# a and b
class LogicalAnd(BaseBooleanCompare):
    def __init__(self, left, right):
        super(LogicalAnd, self).__init__()
        self.type = NodeType.LogicalAnd_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " AND " + str(self.right)

    def clone(self):
        bc = LogicalAnd(None, None)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a or b
class LogicalOr(BaseBooleanCompare):
    def __init__(self, left, right):
        super(LogicalOr, self).__init__()
        self.type = NodeType.LogicalOr_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " OR " + str(self.right)

    def clone(self):
        bc = LogicalOr(None, None)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a || b
# 注意，还可以是字符串连接，此时返回结果不是bool
class LogicalConcat(BaseBooleanCompare):
    def __init__(self, left, right):
        super(LogicalConcat, self).__init__()
        self.type = NodeType.LogicalConcat_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " || " + str(self.right)

    def clone(self):
        bc = LogicalConcat(None, None)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a IS NULL
# a IS NOT NULL
class LogicalIsNull(BooleanCompare):
    def __init__(self):
        super(LogicalIsNull, self).__init__()
        self.type = NodeType.LogicalIsNull_EXPR
        self.expr = None
        self.notFlag = False

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        if self.notFlag:
            return "isNotNull(" + str(self.expr) + ")"
        else:
            return "isNull(" + str(self.expr) + ")"

    def clone(self):
        bc = LogicalIsNull()
        if hasattr(self.expr, "clone"):
            bc.expr = self.expr.clone()
        else:
            bc.expr = self.expr

        return bc


# A IS [NOT] (TRUE|FALSE)
class LogicalIsTrue(BooleanCompare):
    def __init__(self):
        super(LogicalIsTrue, self).__init__()
        self.type = NodeType.LogicalIsTrue_EXPR
        self.expr = None
        self.not_flag = False
        self.value_flag = True

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        if self.value_flag is True:
            value = "TRUE "
        else:
            value = "FALSE "

        if self.not_flag:
            return str(self.expr) + " IS NOT " + value
        else:
            return str(self.expr) + " IS " + value

    def clone(self):
        bc = LogicalIsTrue()
        if hasattr(self.expr, "clone"):
            bc.expr = self.expr.clone()
        else:
            bc.expr = self.expr

        return bc


# a <= b
# a >= b
# a < b
# a > b
class LogicalCompare(BaseBooleanCompare):
    def __init__(self, left, right, ooperator):
        super(LogicalCompare, self).__init__()
        self.type = NodeType.LogicalCompare_EXPR
        self.left = left
        self.right = right
        self.operator = ooperator

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        if self.operator == OperatorType.LE:
            op = " <= "
        elif self.operator == OperatorType.GE:
            op = " >= "
        elif self.operator == OperatorType.LT:
            op = " < "
        else:
            op = " > "

        return str(self.left) + op + str(self.right)

    def clone(self):
        bc = LogicalCompare(None, None, self.operator)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a IN b , The in(a, b) function
# a NOT IN b , The notIn(a, b) function
# a GLOBAL IN b , The globalIn(a, b) function
# a GLOBAL NOT IN b , The globalNotIn(a, b) function
class LogicalIn(BooleanCompare):
    def __init__(self, left, right, in_type):
        super(LogicalIn, self).__init__()
        self.type = NodeType.LogicalIn_EXPR
        self.left = left
        self.right = right
        self.in_type = in_type

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        if self.in_type == LogicalInType.GLOBAL_IN:
            return str(self.left) + " GLOBAL IN " + str(self.right)
        elif self.in_type == LogicalInType.GLOBAL_NOT_IN:
            return str(self.left) + " GLOBAL NOT IN " + str(self.right)
        elif self.in_type == LogicalInType.IN:
            return str(self.left) + " IN " + str(self.right)
        else:
            return str(self.left) + " NOT IN " + str(self.right)

    def clone(self):
        bc = LogicalIn(None, None, self.in_type)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a like b, The like(a, b) function
# a not like b , The notLike(a, b) function.
# a ilike b, The ilike(a, b) function
# a not ilike b , The notILike(a, b) function
class LogicalLike(BooleanCompare):
    def __init__(self, left, right, like_type):
        super(LogicalLike, self).__init__()
        self.type = NodeType.LogicalLike_EXPR
        self.left = left
        self.right = right
        self.like_type = like_type

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        if self.like_type == LogicalLikeType.NOT_LIKE:
            return str(self.left) + " not like " + str(self.right)
        elif self.like_type == LogicalLikeType.NOT_ILIKE:
            return str(self.left) + " not ilike " + str(self.right)
        elif self.like_type == LogicalLikeType.LIKE:
            return str(self.left) + " like " + str(self.right)
        else:
            return str(self.left) + " ilike " + str(self.right)

    def clone(self):
        bc = LogicalLike(None, None, self.like_type)
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


# a BETWEEN b AND c – The same as a >= b AND a <= c
# a NOT BETWEEN b AND c – The same as a < b OR a > c
class LogicalBetween(BooleanCompare):
    def __init__(self):
        super(LogicalBetween, self).__init__()
        self.type = NodeType.LogicalBetween_EXPR
        self.value = None
        self.not_flag = None
        self.lower_bound = None
        self.upper_bound = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.value.accept(visitor)
        self.lower_bound.accept(visitor)
        self.upper_bound.accept(visitor)

    def __str__(self):
        if self.not_flag:
            return str(self.value) + " NOT BETWEEN " + str(self.lower_bound) + " AND " + str(self.upper_bound)
        else:
            return str(self.value) + " BETWEEN " + str(self.lower_bound) + " AND " + str(self.upper_bound)

    def clone(self):
        bc = LogicalBetween()
        if hasattr(self.left, "clone"):
            bc.left = self.left.clone()
        else:
            bc.left = self.left

        if hasattr(self.right, "clone"):
            bc.right = self.right.clone()
        else:
            bc.right = self.right

        return bc


def parse_bool(v):
    if isinstance(v, bool):
        return v
    elif isinstance(v, (int, float, np.int)):
        if float(v) == 0.0:
            return False
        elif float(v) == 1.0:
            return True
        else:
            return v
    elif isinstance(v, str):
        if v.lower() == "true" or v == "1":
            return True
        elif v.lower() == "false" or v == "0":
            return False
        else:
            return v
