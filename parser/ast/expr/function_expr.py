# This file may have been modified by Beijing Volcano Engine Technology Ltd. (“ Volcano Engine's Modifications”).
# All Volcano Engine's Modifications are Copyright (2023) Beijing Volcano Engine Technology Ltd.

from parser.ast.base import SqlExpr, Seq, sensitivity_internal
from parser.ast.type.node_type import NodeType
import numpy as np

funcs = {
    "abs": np.abs,
    "ceiling": np.ceil,
    "floor": np.floor,
    "sign": np.sign,
    "sqrt": np.sqrt,
    "square": np.square,
    "exp": np.exp,
    "log": np.log,
    "log10": np.log10,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "asin": np.arcsin,
    "acos": np.arccos,
    "atan": np.arctan,
    "degrees": np.degrees,
}

bare_funcs = {
    "pi": lambda: np.pi,
    "rand": lambda: np.random.uniform(),
    "random": lambda: np.random.uniform(),
    "newid": lambda: "-".join(
        [
            "".join([hex(np.random.randint(0, 65535)) for v in range(2)]),
            [hex(np.random.randint(0, 65535))],
            [hex(np.random.randint(0, 65535))],
            [hex(np.random.randint(0, 65535))],
            "".join([hex(np.random.randint(0, 65535)) for v in range(3)]),
        ]
    ),
}

op = {
    "plus": "+",
    "minus": "-",
    "multiply": "*",
    "modulo": "%"
}


class Function(SqlExpr):
    def __init__(self):
        super(Function, self).__init__()
        self.func_name = None


class CommonFunction(Function):
    def __init__(self, name):
        super(CommonFunction, self).__init__()
        self.type = NodeType.CommonFunction_EXPR
        self.func_name = name
        self.column_list = Seq(self)
        self.distinct_flag = None
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for column in self.column_list:
            column.accept(visitor)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        if len(self.column_list) > 0:
            column_info = "(" + ", ".join([str(c) for c in self.column_list if c is not None]) + ")"
        else:
            column_info = ""

        return str(self.func_name) + column_info + "(" + ", ".join([str(c) for c in self.args if c is not None]) + ")"

    def sensitivity(self):
        return self.args.sensitivity()

    def dbtype(self, converter):
        funcname = str(self.func_name)
        # 算数运算类型函数单独处理
        if funcname.lower() in ["plus", "minus", "multiply", "modulo"]:
            l_tn = self.args[0].dbtype(converter)
            r_tn = self.args[1].dbtype(converter)
            return converter.op_dbtype(op[funcname.lower()], l_tn, r_tn)
        dbtype = converter.function_dbtype(funcname)
        return dbtype

    def type(self):
        # TODO: use converter if necessary
        return "unknown"

    def clone(self):
        cf = CommonFunction(None)
        cf.func_name = self.func_name
        cf.distinct_flag = self.distinct_flag
        for col in self.column_list:
            cf.column_list.append(col.clone())
        for arg in self.args:
            cf.args.append(arg.clone())

        return cf


MATH_FUNCTION = [
    "ABS",
    "NEGATE",
    "GCD",
    "LCM",
]

SUPPORTED_MATH_FUNCTION = [
    "ABS",
    "NEGATE",
]


SUPPORTED_INNER_FUNCTION = [
    "toInt8",
    "toInt16",
    "toInt32",
    "toInt64",
    "toInt8OrZero",
    "toInt16OrZero",
    "toInt32OrZero",
    "toInt64OrZero",
    "toInt8OrNull",
    "toInt16OrNull",
    "toInt32OrNull",
    "toInt64OrNull",
    "toUInt8",
    "toUInt16",
    "toUInt32",
    "toUInt64",
    "toFloat32",
    "toFloat64",
    "toFloat32OrZero",
    "toFloat64OrZero",
    "toFloat32OrNull",
    "toFloat64OrNull",
    "reinterpretAsUInt8",
    "reinterpretAsUInt16",
    "reinterpretAsUInt32",
    "reinterpretAsUInt64",
    "reinterpretAsInt8",
    "reinterpretAsInt16",
    "reinterpretAsInt32",
    "reinterpretAsInt64",
    "reinterpretAsFloat32",
    "reinterpretAsFloat64",
    "reinterpretAsDate",
    "reinterpretAsDateTime",
    "reinterpretAsString",
    "reinterpretAsFixedString",
    "toDate",
    "toDateOrZero",
    "toDateOrNul",
    "toDateTime",
    "toString",
    "toFixedString",
    "toStringCutToZero",
    "transform",
]


# ABS | CEILING | FLOOR | SIGN | SQRT | SQUARE | EXP | LOG | LOG10 | SIN | COS | TAN | ASIN | ACOS | ATAN  | DEGREES
class MathFunction(Function):
    def __init__(self, name):
        super(MathFunction, self).__init__()
        self.type = NodeType.MathFunction_EXPR
        self.func_name = name
        self.db_type = None
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return str(self.func_name) + "(" + ", ".join([str(c) for c in self.args if c is not None]) + ")"

    def evaluate(self, bindings):
        if len(self.args) == 1:
            exp = self.args[0].evaluate(bindings)
            if exp < 0 and self.func_name.lower() in ['sqrt']:
                return 0
            return funcs[self.func_name.lower()](exp)
        elif len(self.args) == 0:
            return funcs[self.func_name.lower()]()

    def dbtype(self, converter):
        if self.db_type is not None:
            return self.db_type
        return "Float64"

    # Need to add a conversion function to get the type in python according to the db type
    def type(self):
        return "float"

    def clone(self):
        mf = MathFunction(self.func_name)
        for arg in self.args:
            mf.args.append(arg.clone())
        return mf


# PI | RANDOM | RAND | NEWID
class BareFunction(Function):
    def __init__(self, name):
        super(BareFunction, self).__init__()
        self.type = NodeType.BareFunction_EXPR
        self.func_name = name

    def accept0(self, visitor, order):
        pass

    def evaluate(self, bindings):
        vec = bindings[list(bindings.keys())[0]]  # grab the first column
        return [bare_funcs[self.func_name.lower()]() for v in vec]


class RoundFunction(Function):
    def __init__(self):
        super(RoundFunction, self).__init__()
        self.type = NodeType.RoundFunction_EXPR
        self.func_name = "round"
        self.expr = None
        self.number = None

    def accept0(self, visitor, order):
        pass

    def evaluate(self, bindings):
        exp = self.expr.evaluate(bindings)
        return np.round(exp, self.number.value)

    def clone(self):
        rf = RoundFunction()
        rf.expr = self.expr.clone()
        rf.number = self.number.clone()

        return rf


class PowerFunction(Function):
    def __init__(self):
        super(PowerFunction, self).__init__()
        self.type = NodeType.PowerFunction_EXPR
        # pow or power
        self.func_name = "POW"
        self.expr = None
        self.number = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return str(self.func_name) + "(" + str(self.expr) + ", " + str(self.number) + ")"

    def sensitivity(self):
        exp_sens = sensitivity_internal(self.expr)
        if exp_sens is None:
            return None
        return pow(exp_sens, self.number.value.value)

    def evaluate(self, bindings):
        exp = self.expr.evaluate(bindings)
        return np.power(exp, self.number.value.value)

    def dbtype(self, converter):
        return converter.function_dbtype("pow")

    def type(self):
        return self.expr.type()

    def clone(self):
        pf = PowerFunction()
        pf.expr = self.expr.clone()
        pf.number = self.number.clone()

        return pf
