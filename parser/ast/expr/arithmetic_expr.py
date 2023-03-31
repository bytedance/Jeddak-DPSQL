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
from parser.ast.base import SqlExpr, Symbol, sensitivity_internal
from parser.ast.expr.base_expr import Literal, Number
from parser.ast.type.node_type import NodeType

ops = {
    NodeType.AdditionExpression_EXPR: operator.add,
    NodeType.SubtractionExpression_EXPR: operator.sub,
    NodeType.DivideExpression_EXPR: operator.truediv,
    NodeType.MultiplyExpression_EXPR: operator.mul,
    NodeType.ModuloExpression_EXPR: operator.mod,
}

op = {
    NodeType.AdditionExpression_EXPR: "+",
    NodeType.SubtractionExpression_EXPR: "-",
    NodeType.DivideExpression_EXPR: "/",
    NodeType.MultiplyExpression_EXPR: "*",
    NodeType.ModuloExpression_EXPR: "%",
}


class ArithmeticExpression(SqlExpr):
    def __init__(self):
        super(ArithmeticExpression, self).__init__()
        self.type = NodeType.ArithmeticExpression_EXPR
        self.symbol = Symbol()

    def accept0(self, visitor, order):
        pass


# -a , The negate (a) function
class NegateExpression(ArithmeticExpression):
    def __init__(self):
        super(NegateExpression, self).__init__()
        self.type = NodeType.NegateExpression_EXPR
        self.expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return "-" + str(self.expr)

    def clone(self):
        ae = NegateExpression()
        ae.symbol = self.symbol
        if hasattr(self.expr, "clone"):
            ae.expr = self.expr.clone()
        else:
            ae.expr = self.expr

        return ae


class BinocularOperation(ArithmeticExpression):
    def sensitivity(self):
        ls = sensitivity_internal(self.left)
        rs = sensitivity_internal(self.right)
        if rs is None and ls is None:
            return None
        if rs is None and type(self.right) is Literal and type(self.right.value) is Number:
            if self.type in [NodeType.AdditionExpression_EXPR, NodeType.SubtractionExpression_EXPR]:
                return ls
            elif self.type == NodeType.ModuloExpression_EXPR:
                return self.right.value.value
            elif self.type == NodeType.MultiplyExpression_EXPR:
                return ls * self.right.value.value
            elif self.type == NodeType.DivideExpression_EXPR:
                return ls / self.right.value.value
            else:
                return None
        if ls is None and type(self.left) is Literal and type(self.left.value) is Number:
            if self.type in [NodeType.AdditionExpression_EXPR, NodeType.SubtractionExpression_EXPR]:
                return rs
            elif self.type == NodeType.MultiplyExpression_EXPR:
                return rs * self.left.value.value
            else:
                return None
        if ls is not None and rs is not None:
            if self.type == NodeType.AdditionExpression_EXPR:
                return ls + rs
            elif self.type == NodeType.MultiplyExpression_EXPR:
                return ls * rs
            else:
                return None

    def evaluate(self, bindings):
        left = self.left.evaluate(bindings)
        right = self.right.evaluate(bindings)
        # "" empty string is used to represent null
        # TODO: handle more elegant way
        if left == '' or right == '':
            return ''
        if right == 0 and self.type == NodeType.DivideExpression_EXPR:
            return 0
        return ops[self.type](left, right)

    def dbtype(self, converter):
        l_tn = self.left.dbtype(converter)
        r_tn = self.right.dbtype(converter)
        return converter.op_dbtype(op[self.type], l_tn, r_tn)

    # a * b – The multiply (a, b) function.

    def type(self):
        if op[self.type] == "/":
            return "float"
        elif op[self.type] == "%":
            return "int"
        elif op[self.type] in ["*", "+", "-"]:
            return min([self.left.type(), self.right.type()])


class MultiplyExpression(BinocularOperation):
    def __init__(self, left, right):
        super(MultiplyExpression, self).__init__()
        self.type = NodeType.MultiplyExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return "(" + str(self.left) + " )" + " * " + "(" + str(self.right) + " )"

    def clone(self):
        ae = MultiplyExpression(None, None)
        ae.symbol = self.symbol
        if hasattr(self.left, "clone"):
            ae.left = self.left.clone()
        else:
            ae.left = self.left

        if hasattr(self.right, "clone"):
            ae.right = self.right.clone()
        else:
            ae.right = self.right

        return ae


# a / b – The divide(a, b) function.
class DivideExpression(BinocularOperation):
    def __init__(self, left, right):
        super(DivideExpression, self).__init__()
        self.type = NodeType.DivideExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + "/" + str(self.right)

    def clone(self):
        ae = DivideExpression(None, None)
        ae.symbol = self.symbol
        if hasattr(self.left, "clone"):
            ae.left = self.left.clone()
        else:
            ae.left = self.left

        if hasattr(self.right, "clone"):
            ae.right = self.right.clone()
        else:
            ae.right = self.right

        return ae


# a % b – The modulo(a, b) function
class ModuloExpression(BinocularOperation):
    def __init__(self, left, right):
        super(ModuloExpression, self).__init__()
        self.type = NodeType.ModuloExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + "%" + str(self.right)

    def clone(self):
        ae = ModuloExpression(None, None)
        ae.symbol = self.symbol
        if hasattr(self.left, "clone"):
            ae.left = self.left.clone()
        else:
            ae.left = self.left

        if hasattr(self.right, "clone"):
            ae.right = self.right.clone()
        else:
            ae.right = self.right

        return ae


# Gives the integer part resulting from dividing A by B.
# E.g 17 div 3 results in 5
class DivExpression(BinocularOperation):
    def __init__(self, left, right):
        super(DivExpression, self).__init__()
        self.type = NodeType.DivExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " div " + str(self.right)

    def clone(self):
        de = DivExpression(None, None)
        de.symbol = self.symbol
        if hasattr(self.left, "clone"):
            de.left = self.left.clone()
        else:
            de.left = self.left

        if hasattr(self.right, "clone"):
            de.right = self.right.clone()
        else:
            de.right = self.right

        return de


# a + b – The plus(a, b) function
class AdditionExpression(BinocularOperation):
    def __init__(self, left, right):
        super(AdditionExpression, self).__init__()
        self.type = NodeType.AdditionExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " + " + str(self.right)

    def clone(self):
        ae = AdditionExpression(None, None)
        ae.symbol = self.symbol
        if hasattr(self.left, "clone"):
            ae.left = self.left.clone()
        else:
            ae.left = self.left

        if hasattr(self.right, "clone"):
            ae.right = self.right.clone()
        else:
            ae.right = self.right

        return ae


# a - b – The minus(a, b) function
class SubtractionExpression(BinocularOperation):
    def __init__(self, left, right):
        super(SubtractionExpression, self).__init__()
        self.type = NodeType.SubtractionExpression_EXPR
        self.left = left
        self.right = right

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return str(self.left) + " - " + str(self.right)

    def clone(self):
        ae = SubtractionExpression(None, None)
        ae.symbol = self.symbol
        if hasattr(self.left, "clone"):
            ae.left = self.left.clone()
        else:
            ae.left = self.left

        if hasattr(self.right, "clone"):
            ae.right = self.right.clone()
        else:
            ae.right = self.right

        return ae
