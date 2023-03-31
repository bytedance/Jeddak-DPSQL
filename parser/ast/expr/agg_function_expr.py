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

from parser.ast.base import Symbol, Seq
from parser.ast.expr.function_expr import Function
from parser.ast.type.node_type import NodeType


class SqlAggFunction(Function):
    def __init__(self):
        super(SqlAggFunction, self).__init__()
        self.symbol = Symbol()
        self.flag_type = None
        self.args = Seq(self)
        self.type = NodeType.SqlAggFunction_EXPR

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        if self.flag_type is not None:
            flag_info = self.flag_type.name + " "
        else:
            flag_info = ""
        return str(self.func_name) + "(" + flag_info + ",".join(str(c) for c in self.args) + ")"

    def clone(self):
        saf = SqlAggFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)

        return saf

    def evaluate(self, bindings):
        # need to decide what to do with this
        if len(self.args) > 0:
            return self.args.evaluate(bindings)
        else:
            if str(self).lower() in bindings:
                return bindings[str(self).lower()]
            else:
                return None

    # 似乎不需要分这么细，待细考虑

    def dbtype(self, converter):
        if self.type in [NodeType.SqlVarPopFunction_EXPR, NodeType.SqlStdPopFunction_EXPR,
                         NodeType.SqlAvgFunction_EXPR]:
            return converter.function_dbtype(self.func_name.lower())
        else:
            return "unknown"

    def type(self):
        if self.type in [NodeType.SqlVarPopFunction_EXPR, NodeType.SqlStdPopFunction_EXPR,
                         NodeType.SqlAvgFunction_EXPR]:
            return "float"
        else:
            return "unknown"


class SqlCountFunction(SqlAggFunction):
    def __init__(self):
        super(SqlCountFunction, self).__init__()
        self.type = NodeType.SqlCountFunction_EXPR
        self.func_name = "COUNT"
        # Can be exclusive to count, clickhouse
        self.symbol.sens = 1

    def sensitivity(self):
        return 1

    def clone(self):
        saf = SqlCountFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)

        return saf

    def dbtype(self, converter):
        return converter.function_dbtype("count")

    def type(self):
        return "int"


class SqlMinFunction(SqlAggFunction):
    def __init__(self):
        super(SqlMinFunction, self).__init__()
        self.type = NodeType.SqlMinFunction_EXPR
        self.func_name = "MIN"

    def sensitivity(self):
        return self.args.sensitivity()

    def clone(self):
        saf = SqlMinFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)
        return saf

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()


class SqlMaxFunction(SqlAggFunction):
    def __init__(self):
        super(SqlMaxFunction, self).__init__()
        self.type = NodeType.SqlMaxFunction_EXPR
        self.func_name = "MAX"

    def sensitivity(self):
        return self.args.sensitivity()

    def clone(self):
        saf = SqlMaxFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)

        return saf

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()


class SqlSumFunction(SqlAggFunction):
    def __init__(self):
        super(SqlSumFunction, self).__init__()
        self.type = NodeType.SqlSumFunction_EXPR
        self.func_name = "SUM"
        self.args_type = None

    def sensitivity(self):
        return self.args.sensitivity()

    def clone(self):
        saf = SqlSumFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)

        return saf

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()


class SqlAvgFunction(SqlAggFunction):
    def __init__(self):
        super(SqlAvgFunction, self).__init__()
        self.type = NodeType.SqlAvgFunction_EXPR
        self.func_name = "AVG"
        # # must be Integer, Float, or Decimal.
        # self.value = value

    def sensitivity(self):
        return self.args.sensitivity()

    def clone(self):
        saf = SqlAvgFunction()
        saf.symbol = self.symbol
        saf.flag_type = self.flag_type
        for arg in self.args:
            arg1 = arg.clone()
            saf.args.append(arg1)

        return saf

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()


# population variance
class SqlVarPopFunction(SqlAggFunction):
    def __init__(self):
        super(SqlVarPopFunction, self).__init__()
        self.type = NodeType.SqlVarPopFunction_EXPR
        self.func_name = "varPop"
        # self.func_name = "var"

    def sensitivity(self):
        return self.args.sensitivity()

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()


class SqlStdPopFunction(SqlAggFunction):
    def __init__(self):
        super(SqlStdPopFunction, self).__init__()
        self.type = NodeType.SqlStdPopFunction_EXPR
        self.func_name = "stddevPop"
        # self.func_name = "stddev"

    def sensitivity(self):
        return self.args.sensitivity()

    def dbtype(self, converter):
        return self.args.dbtype(converter)

    def type(self):
        return self.args.type()
