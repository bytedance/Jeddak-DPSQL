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

from parser.ast.base import SqlExpr, Symbol, Seq
from parser.ast.expr.logical_bool import LogicalEqual
from parser.ast.type.node_type import NodeType
import numpy as np
from parser.utils.common_utils import unique


class CondExpression(SqlExpr):
    def __init__(self):
        super(CondExpression, self).__init__()
        self.type = NodeType.CondExpression_EXPR
        self.symbol = Symbol()

    def accept0(self, visitor, order):
        pass

    def dbtype(self, converter):
        if self.symbol is not None:
            return self.symbol.dbtype(converter)


# if(cond, then, else)
class IfExpression(CondExpression):
    def __init__(self):
        super(IfExpression, self).__init__()
        self.type = NodeType.IfExpression_EXPR
        self.cond = None
        self.then_expr = None
        self.else_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        if self.cond is not None:
            self.cond.accept(visitor)
        if self.then_expr is not None:
            self.then_expr.accept(visitor)
        if self.else_expr is not None:
            self.else_expr.accept(visitor)

    def __str__(self):
        return "if(" + str(self.cond) + "," + str(self.then_expr) + "," + str(self.else_expr) + ")"

    def sensitivity(self):
        t = [self.then_expr.sensitivity()] if self.then_expr is not None else []
        t = t + [self.else_expr.sensitivity()]
        t = [s for s in t if s is not None]
        if len(t) > 0:
            return max(t)
        else:
            return None

    def dbtype(self, converter):
        t = [self.then_expr.dbtype(converter)]
        if len(unique(t)) == 1:
            return t[0]
        # FIXME
        return converter.op_dbtype('-', unique(t)[0], unique(t)[1])

    def type(self):
        t = [self.else_expr.type()] if self.else_expr is not None else []
        t = t + [self.then_expr.type()]
        if len(unique(t)) == 1:
            return t[0]
        elif "string" in t:
            return "string"
        elif sorted(unique(t)) == ["float", "int"]:
            return "float"
        else:
            return "unknown"


class IIFFunction(CondExpression):
    def __init__(self):
        super(IIFFunction, self).__init__()
        self.type = NodeType.IIFFunction_EXPR
        self.cond = None
        self.then_expr = None
        self.else_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        if self.cond is not None:
            self.cond.accept(visitor)
        if self.then_expr is not None:
            self.then_expr.accept(visitor)
        if self.else_expr is not None:
            self.else_expr.accept(visitor)

    def __str__(self):
        return "iif(" + str(self.cond) + "," + str(self.then_expr) + "," + str(self.else_expr) + ")"


# multiIf(cond_1, then_1, cond_2, then_2, ..., else)
class MultiIfExpression(CondExpression):
    def __init__(self):
        super(MultiIfExpression, self).__init__()
        self.type = NodeType.MultiIfExpression_EXPR
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return "multiIf(" + " , ".join([str(c) for c in self.args if c is not None]) + ")"

    def dbtype(self, converter):
        t = [self.args.dbtype(converter)] if self.args is not None else []
        if len(unique(t)) == 1:
            return t[0]
        # FIXME
        return converter.op_dbtype('-', unique(t)[0], unique(t)[1])

    def sensitivity(self):
        t = [self.args.sensitivity()] if self.args is not None else []
        if len(t) > 0:
            return max(t)
        else:
            return None


# CASE [x]
#     WHEN a THEN b
#     [WHEN ... THEN ...]
#     [ELSE c]
# END
# If x is specified, then transform(x, [a, ...], [b, ...], c) function is used. Otherwise – multiIf(a, b, ..., c).
#
# If there is no ELSE c clause in the expression, the default value is NULL.
#
# The transform function does not work with NULL.
class CaseExpression(CondExpression):
    def __init__(self):
        super(CaseExpression, self).__init__()
        self.type = NodeType.CaseExpression_EXPR
        self.case_expr = None
        # 可能有多个
        self.when_exprs = Seq(self)
        self.else_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        if self.case_expr is not None:
            self.case_expr.accept(visitor)
        for when_expr in self.when_exprs:
            when_expr.accept(visitor)
        if self.else_expr is not None:
            self.else_expr.accept(visitor)

    def __str__(self):
        case_info = str(self.case_expr) + " " if self.case_expr is not None else " "
        else_info = " ELSE " + str(self.else_expr) if self.else_expr is not None else ""
        return "CASE " + case_info + " ".join(str(c) for c in self.when_exprs) + str(else_info) + " END"

    def sensitivity(self):
        t = [self.else_expr.sensitivity()] if self.else_expr is not None else []
        t = t + [we.sensitivity() for we in self.when_exprs]
        t = [s for s in t if s is not None]
        if len(t) > 0:
            return max(t)
        else:
            return None

    def evaluate(self, bindings):
        else_exp = self.else_expr.evaluate(bindings)
        res = np.repeat(else_exp, len(bindings[list(bindings.keys())[0]]))
        if self.case_expr is not None:
            # simple search
            for we in self.when_exprs:
                match = LogicalEqual(self.case_expr, "=", we.args).evaluate(bindings)
                res[match] = we.then_expr.evaluate(bindings)
        else:
            # regular search
            for we in self.when_exprs:
                match = we.args.evaluate(bindings)
                res[match] = we.then_expr.evaluate(bindings)
        return res

    def dbtype(self, converter):
        t = [self.else_expr.dbtype(converter)] if self.else_expr is not None else []
        t = t + [we.dbtype(converter) for we in self.when_exprs]
        if len(unique(t)) == 1:
            return t[0]
        # FIXME
        return converter.op_dbtype('-', unique(t)[0], unique(t)[1])

    def type(self):
        t = [self.else_expr.type()] if self.else_expr is not None else []
        t = t + [we.type() for we in self.when_exprs]
        if len(unique(t)) == 1:
            return t[0]
        elif "string" in t:
            return "string"
        elif sorted(unique(t)) == ["float", "int"]:
            return "float"
        else:
            return "unknown"


class WhenExpression(CondExpression):
    def __init__(self):
        super(WhenExpression, self).__init__()
        self.type = NodeType.WhenExpression_EXPR
        self.when_expr = None
        self.then_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.when_expr.accept(visitor)
        self.then_expr.accept(visitor)

    def __str__(self):
        return "WHEN " + str(self.when_expr) + " THEN " + str(self.then_expr)

    def sensitivity(self):
        return self.then_expr.sensitivity()

    def evaluate(self, bindings):
        if self.args.evaluate(bindings):
            return self.then_expr.evaluate(bindings)
        else:
            return None

    def dbtype(self, converter):
        return self.then_expr.dbtype(converter)

    def type(self):
        return self.then_expr.type()


# cond ? then : else
class TernaryExpression(CondExpression):
    def __init__(self):
        super(TernaryExpression, self).__init__()
        self.type = NodeType.TernaryExpression_EXPR
        self.cond_expr = None
        self.then_expr = None
        self.else_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.cond_expr.accept(visitor)
        self.then_expr.accept(visitor)
        self.else_expr.accept(visitor)

    def __str__(self):
        return str(self.cond_expr) + " ? " + str(self.then_expr) + " : " + str(self.else_expr)


class CoalesceFuncExpression(CondExpression):
    def __init__(self):
        super(CoalesceFuncExpression, self).__init__()
        self.type = NodeType.CoalesceFunction_EXPR
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return "COALESCE(" + ", ".join([str(c) for c in self.args if c is not None]) + ")"
