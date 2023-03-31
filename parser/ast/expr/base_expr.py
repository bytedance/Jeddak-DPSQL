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

from parser.ast.base import SqlExpr, Seq, ColumnInfo, SqlNode, MapExpressionInfo

# constants, including：numberLiteral 、STRING_LITERAL 、NULL
# todo further subdivided
from parser.ast.type.node_type import NodeType, ExprAliasType, LiteralType, DialectType


class Literal(SqlExpr):
    def __init__(self, value=None):
        super(Literal, self).__init__()
        self.type = NodeType.Literal_EXPR
        self.value = value
        self.type = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        if self.type == LiteralType.STRING_LITERAL:
            return self.value
        elif self.type == LiteralType.NUM_LITERAL:
            return str(self.value)
        else:
            return "NULL"

    def clone(self):
        literal = Literal()
        if hasattr(self.value, "clone"):
            literal.value = self.value.clone()
        else:
            literal.value = self.value
        literal.type = self.type
        return literal

    def dbtype(self, converter):
        return converter.litral_dbtype(type(self.value.value).__name__, self.value)
        # return converter.litral_dbtype(self.type, self.value)
        # else:
        #     return converter.litral_dbtype(self.value.type(), self.value)
        # if self.type() not in ["string", "float", "int", "boolean"]:
        #     return converter.litral_dbtype(self.value.type(), self.value)
        # return converter.litral_dbtype(self.type(), self.value)

    def type(self):
        if isinstance(self.value, str):
            return "string"
        elif type(self.value) is float:
            return "float"
        elif type(self.value) is int:
            return "int"
        elif type(self.value) is bool:
            return "boolean"
        else:
            raise ValueError("Unknown literal type: " + str(type(self.value)))

    def evaluate(self, bindings):
        if str(self.parent).lower() in bindings:
            return bindings[str(self.parent).lower()]
        else:
            return None


class SymbolState:
    def __init__(self):
        # whether its source contains an aggregate function
        self.agg_flag = False
        self.arith_flag = False
        self.name = None
        # Its source symbolic expression, if it comes directly from the physical table, this item is empty
        self.src_expr = []
        self.symbol_link_flag = False
        # The corresponding information related to noise addition, such as its upper and lower bounds, sensitivity, etc., needs a new structure to represent
        self.noise_info = None


# Identifier
class Identifier(SqlExpr):
    def __init__(self, text):
        super(Identifier, self).__init__()
        self.type = NodeType.Identifier_EXPR
        self.text = text
        self.symbol = None
        # Symbol State instance, describing the current symbol state, such as whether the source of the aggregation function, the previous aggregation propagation point (similar to taint analysis)
        self.state = SymbolState()

    def __str__(self):
        return self.text

    def accept0(self, visitor, order):
        visitor.visit(self)

    def sensitivity(self):
        if hasattr(self, "state"):
            if len(self.state.src_expr) > 0:
                column_info = self.state.src_expr[0].column_info
                if column_info.common_column_info is not None and column_info.common_column_info.maxval is not None and column_info.common_column_info.minval is not None:
                    return column_info.common_column_info.maxval - column_info.common_column_info.minval
                else:
                    return None
        if self.symbol is not None:
            return self.symbol.sensitivity()
        return None

    def evaluate(self, bindings):
        if self.text.lower() in bindings:
            return bindings[self.text.lower()]
        elif str(self.parent).lower() in bindings:
            return bindings[str(self.parent).lower()]
        else:
            return None

    def clone(self):
        ident = Identifier(self.text)
        ident.symbol = self.symbol
        ident.state = self.state
        return ident

    def dbtype(self, converter):
        if self.symbol is not None:
            return self.symbol.dbtype(converter)
        return None


# Value
class Number(SqlExpr):
    def __init__(self, value):
        super(Number, self).__init__()
        self.type = NodeType.Number_EXPR
        self.value = value
        self.type = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return str(self.value)

    def clone(self):
        num = Number(self.value)
        num.type = self.type
        return num


# Represents the fields of the data table
class Column(SqlExpr):
    def __init__(self, table, column):
        super(Column, self).__init__()
        self.type = NodeType.Column_EXPR
        # Identifier name
        self.table = table
        self.column = column
        self.column_info = ColumnInfo()

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        if self.table is not None:
            return str(self.table) + "." + str(self.column)
        else:
            return str(self.column)

    def clone(self):
        col = Column(None, None)
        if self.table is not None:
            col.table = self.table.clone()
        col.column = self.column.clone()
        return col


# *
class AllColumns(SqlExpr):
    def __init__(self):
        super(AllColumns, self).__init__()
        self.type = NodeType.AllColumns_EXPR

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return "*"

    def evaluate(self, bindings):
        if str(self.parent).lower() in bindings:
            return bindings[str(self.parent).lower()]
        else:
            return None

    def clone(self):
        all_column = AllColumns()
        return all_column


# a[N] – Access to an element of an array.
# clickhouse : equas arrayElement(a, N) function.
# hive : access to array or map
class ArrayAccess(SqlExpr):
    def __init__(self):
        super(ArrayAccess, self).__init__()
        self.type = NodeType.ArrayAccess_EXPR
        self.array = None
        self.key = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return str(self.array) + "[" + str(self.key) + "]"

    def clone(self):
        aa = ArrayAccess()
        aa.array = self.array.clone()
        aa.key = self.key.clone() if isinstance(self.key, SqlNode) else self.key

        return aa


# a.N – Access to a tuple element. The tupleElement(a, N) function
class TupleAccess(SqlExpr):
    def __init__(self):
        super(TupleAccess, self).__init__()
        self.type = NodeType.TupleAccess_EXPR
        self.tuple = None
        self.number = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return str(self.tuple) + "." + str(self.number)

    def clone(self):
        ta = TupleAccess()
        ta.tuple = self.tuple.clone()
        ta.number = self.number.clone()

        return ta


# [x1, ...] – The array(x1, ...) function
class Arrays(SqlExpr):
    def __init__(self):
        super(Arrays, self).__init__()
        self.type = NodeType.Arrays_EXPR
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return "[" + ",".join(str(c) for c in self.args) + "]"

    def clone(self):
        array = Arrays()
        for arg in self.args:
            new_arg = arg.clone() if isinstance(arg, SqlNode) else arg
            array.args.append(new_arg)

        return array


# (x1, x2, ...) – The tuple(x2, x2, ...) function
class Tuples(SqlExpr):
    def __init__(self):
        super(Tuples, self).__init__()
        self.type = NodeType.Tuples_EXPR
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return "(" + ",".join(str(c) for c in self.args) + ")"

    def clone(self):
        tuples = Tuples()
        for arg in self.args:
            new_arg = arg.clone() if isinstance(arg, SqlNode) else arg
            tuples.args.append(new_arg)

        return tuples


# (key1 : value1, key2 : value2, ...)
# map data collection
class Maps(SqlExpr):
    def __init__(self):
        super(Maps, self).__init__()
        self.type = NodeType.Maps_EXPR
        # Each arg is a key: value form
        self.args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.args:
            arg.accept(visitor)

    def __str__(self):
        return "(" + ",".join(str(c) for c in self.args) + ")"

    def clone(self):
        maps = Maps()
        for arg in self.args:
            new_arg = arg.clone() if isinstance(arg, SqlNode) else arg
            maps.args.append(new_arg)

        return maps


# representative data sheet
class Table(SqlExpr):
    def __init__(self, database, table):
        super(Table, self).__init__()
        self.type = NodeType.Table_EXPR
        self.database = database
        self.table = table
        self.columns = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        if self.database is not None:
            return str(self.database) + "." + str(self.table)
        else:
            return str(self.table)


class TableFunctionExpr(SqlExpr):
    def __init__(self):
        super(TableFunctionExpr, self).__init__()
        self.type = NodeType.TableFunction_EXPR
        self.name = None
        self.table_args = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for arg in self.table_args:
            arg.accept(visitor)

    def __str__(self):
        return str(self.name) + "(" + ",".join(str(c) for c in self.table_args) + ")"

    def clone(self):
        tfe = TableFunctionExpr()
        tfe.name = self.name
        for arg in self.table_args:
            new_arg = arg.clone() if isinstance(arg, SqlNode) else arg
            self.table_args.append(new_arg)
        return tfe


# ordinary column as expressions
class NameExpression(SqlExpr):
    def __init__(self):
        super(NameExpression, self).__init__()
        self.expr = None
        self.alias = None
        self.alias_type = ExprAliasType.Unspecified
        self.type = NodeType.NameExpression_EXPR

    def __str__(self):
        if self.alias is not None:
            return str(self.expr) + " AS " + str(self.alias)
        else:
            return str(self.expr)

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)
        if self.alias is not None:
            self.alias.accept(visitor)

    def sensitivity(self):
        return self.expr.sensitivity()

    def evaluate(self, bindings):
        return self.expr.evaluate(bindings)

    def dbtype(self, converter):
        return self.expr.dbtype(converter)

    def type(self):
        return self.expr.type()

    def clone(self):
        ne = NameExpression()
        ne.expr = self.expr.clone()
        if self.alias is not None and isinstance(self.alias, SqlNode):
            ne.alias = self.alias.clone()
        else:
            ne.alias = self.alias

        return ne


# (expr)
class NestedExpression(SqlExpr):
    def __init__(self):
        super(NestedExpression, self).__init__()
        self.type = NodeType.NestedExpression_EXPR
        self.expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return "(" + str(self.expr) + ")"

    def sensitivity(self):
        return self.expr.sensitivity()

    def evaluate(self, bindings):
        # need to decide what to do with this
        return self.expr.evaluate(bindings)

    def dbtype(self, converter):
        return self.expr.dbtype(converter)

    def type(self):
        return self.expr.type()

    def clone(self):
        ne = NestedExpression()
        ne.expr = self.expr.clone()

        return ne


# x -> expr – The lambda (x, expr) function.
class LambdaExpression(SqlExpr):
    def __init__(self):
        super(LambdaExpression, self).__init__()
        self.type = NodeType.LambdaExpression_EXPR
        self.left_list = Seq(self)
        self.right = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.left_list:
            expr.accept(visitor)
        self.right.accept(visitor)

    def __str__(self):
        return "(" + ",".join(str(c) for c in self.left_list) + ") -> " + str(self.right)

    def clone(self):
        le = LambdaExpression()
        for arg in self.left_list:
            new_arg = arg.clone() if isinstance(arg, SqlNode) else arg
            le.left_list.append(new_arg)
        le.right = self.right.clone()
        return le


# Used after select
class SelectItem(SqlExpr):
    def __init__(self):
        super(SelectItem, self).__init__()
        self.expr = None
        self.alias = None
        self.alias_type = ExprAliasType.Unspecified
        self.type = NodeType.SelectItem_EXPR

    def __str__(self):
        if self.alias is not None:
            return str(self.expr) + " AS " + str(self.alias)
        else:
            return str(self.expr)

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)
        if self.alias is not None:
            self.alias.accept(visitor)

    def clone(self):
        si = SelectItem()
        si.expr = self.expr.clone()
        if self.alias is not None and isinstance(self.alias, SqlNode):
            si.alias = self.alias.clone()
        else:
            si.alias = self.alias

        return si


# The form in clickhouse is: a{b}
# The form in hive is: a[b]
class MapExpression(SqlExpr):
    def __init__(self):
        super(MapExpression, self).__init__()
        self.type = NodeType.MapExpression_EXPR
        self.dialect_type = None
        self.map_name = None
        self.map_key = None
        self.map_info = MapExpressionInfo()

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        if self.dialect_type == DialectType.HIVE:
            return str(self.map_name) + "[" + str(self.map_key) + "]"
        else:
            return str(self.map_name) + "{" + str(self.map_key) + "}"

    def clone(self):
        me = MapExpression()
        me.map_name = self.map_name.clone()
        me.map_key = self.map_key
        me.map_info = self.map_info
        return me

    def sensitivity(self):
        return self.map_info.sensitivity()

    def dbtype(self, converter):
        return self.map_info.dbtype(converter)

    def type(self):
        return self.map_info.type()
