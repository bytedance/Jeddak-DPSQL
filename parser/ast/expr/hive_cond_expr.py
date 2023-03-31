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

from parser.ast.expr.cond_expr import CondExpression
from parser.ast.type.node_type import NodeType


# nvl(T value, T default_value)
# Returns default value if value is null else returns value
class NvlFuncExpression(CondExpression):
    def __init__(self):
        super(NvlFuncExpression, self).__init__()
        self.type = NodeType.Hive_NVLExpression_EXPR
        self.value = None
        self.default_value = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.value.accept(visitor)
        self.default_value.accept(visitor)

    def __str__(self):
        return "nvl( " + str(self.value) + ", " + str(self.default_value) + ")"


# nullif( a, b )
# Returns NULL if a=b; otherwise returns a
class NullIfFuncExpression(CondExpression):
    def __init__(self):
        super(NullIfFuncExpression, self).__init__()
        self.type = NodeType.Hive_NullIfFunction_EXPR
        self.first_arg = None
        self.second_arg = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.first_arg.accept(visitor, order)
        self.second_arg.accept(visitor, order)

    def __str__(self):
        return "nullif(" + str(self.first_arg) + ", " + str(self.second_arg) + ")"


# assert_true(boolean condition)
# Throw an exception if 'condition' is not true, otherwise return null (as of Hive 0.8.0).
# For example, select assert_true (2<1).
class AssertTrueFuncExpression(CondExpression):
    def __init__(self):
        super(AssertTrueFuncExpression, self).__init__()
        self.type = NodeType.Hive_AssertTrueFunction_EXPR
        self.condition = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.condition.accept(visitor, order)

    def __str__(self):
        return "assert_true(" + str(self.condition) + ")"
