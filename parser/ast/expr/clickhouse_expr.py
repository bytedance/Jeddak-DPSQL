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

from parser.ast.base import SqlExpr, Seq
from parser.ast.expr.function_expr import Function
from parser.ast.type.node_type import TimeIntervalType, NodeType


# example : INTERVAL 4 DAY
# https://clickhouse.tech/docs/en/sql-reference/operators/#operator-interval
class Interval(SqlExpr):
    def __init__(self):
        super(Interval, self).__init__()
        self.type = NodeType.Interval_EXPR
        self.value = None
        self.value_type = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        if self.value_type != TimeIntervalType.Unspecified:
            return "INTERVAL " + str(self.value) + " " + str(self.value_type.name)
        else:
            return "INTERVAL " + str(self.value)


# https://clickhouse.com/docs/en/sql-reference/operators/#operator-extract
# EXTRACT(part FROM date);
class ExtractFunction(Function):
    def __init__(self):
        super(ExtractFunction, self).__init__()
        self.type = NodeType.ExtractFunction_EXPR
        self.part = None
        self.date = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.part.accept(visitor)
        self.date.accept(visitor)

    def __str__(self):
        return "EXTRACT(" + str(self.part.name) + " FROM " + str(self.date) + ")"


class TimeStampExpression(SqlExpr):
    def __init__(self):
        super(TimeStampExpression, self).__init__()
        self.str = None

    def accept0(self, visitor, order):
        pass

    def __str__(self):
        return "TIMESTAMP " + str(self.str)


# use commonfunction replace
# class SubStringExpression(SqlExpr):
#     def __init__(self):
#         super(SubStringExpression, self).__init__()
#         self.str = None
#         self.offset = None
#         self.lenth = None
#
#     def __str__(self):
#         return "substring("

# eg :  quantile(level)(expr)、
#       quantileExact(level)(expr)
#       quantileTiming(level)(x)、
#       quantileTDigest(level)(x)
# A series of functions containing the above types
class QuantilesFunction(Function):
    def __init__(self, name):
        super(QuantilesFunction, self).__init__()
        self.type = NodeType.QuantilesFunction_EXPR
        self.func_name = name
        self.level = None
        self.expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.level.accept(visitor)
        self.expr.accept(visitor)


# eg :  quantileDeterministic(level)(x, determinator)、
#       quantileTimingWeighted(level)(x, weight)、
#       quantileExactWeighted(level)(x, weight)
# A series of functions containing the above types
class Quantiles2Function(Function):
    def __init__(self, name):
        super(Quantiles2Function, self).__init__()
        self.type = NodeType.Quantiles2Function_EXPR
        self.func_name = name
        self.level = None
        self.value = None
        self.weight = None

    def accept0(self, visitor, order):
        pass


# quantiles(level1, level2, …)(x)、
# quantilesExactExclusive(level1, level2, ...)(expr)、
# quantilesExactInclusive(level1, level2, ...)(expr)、
class Quantiles3Function(Function):
    def __init__(self, name):
        super(Quantiles3Function, self).__init__()
        self.type = NodeType.Quantiles3Function_EXPR
        self.func_name = name
        self.level_list = []
        self.expr = None

    def accept0(self, visitor, order):
        pass


# func(arg1, arg2...)(va1, va2...)
class ClickHouseCommonFunction(Function):
    def __init__(self, name):
        super(ClickHouseCommonFunction, self).__init__()
        self.type = NodeType.ClickHouseCommonFunction_EXPR
        self.func_name = name
        self.args_list = Seq(self)
        self.val_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args_list:
            arg.accept(visitor)
        for val in self.val_list:
            val.accept(visitor)


# trim([[LEADING|TRAILING|BOTH] trim_character FROM] input_string)
class TrimFunction(Function):
    def __init__(self):
        super(TrimFunction, self).__init__()
        self.type = NodeType.TrimFunction_EXPR
        self.trim_type = None
        self.trim_str = None
        self.input_str = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return "trim(" + str(self.trim_type.name) + " " + str(self.trim_str) + " FROM " + str(self.input_str) + ")"


# todo may be independent
class ColumnsFunction(Function):
    def __init__(self):
        super(ColumnsFunction, self).__init__()
        self.type = NodeType.ColumnsFunction_EXPR
        self.func_name = "COLUMNS"
        self.re_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)


# todo may be independent
class ToTypeNameFunction(Function):
    def __init__(self):
        super(ToTypeNameFunction, self).__init__()
        self.type = NodeType.ToTypeNameFunction_EXPR
        self.func_name = "toTypeName"
        self.expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)


class FormatExpr(SqlExpr):
    def __init__(self):
        super(FormatExpr, self).__init__()
        self.type = NodeType.FormatExpr_EXPR
        self.format_value = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return " FORMAT " + str(self.format_value)
