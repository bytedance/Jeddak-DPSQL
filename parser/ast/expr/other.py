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

from parser.ast.base import SqlExpr, Seq, SqlNode
from parser.ast.type.node_type import LimitSplitType, JoinConstraintType, OrderingType, NodeType

# CAST(1.5 AS Decimal(3,2))


class CastExpr(SqlExpr):
    def __init__(self):
        super(CastExpr, self).__init__()
        self.type = NodeType.CastExpr_EXPR
        self.src_type_expr = None
        self.dest_type_expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.src_type_expr.accept(visitor)
        self.dest_type_expr.accept(visitor)

    def __str__(self):
        return "CAST(" + str(self.src_type_expr) + " AS " + str(self.dest_type_expr) + ")"

    def sensitivity(self):
        return self.src_type_expr.args.sensitivity()

    def clone(self):
        ce = CastExpr()
        ce.src_type_expr = self.src_type_expr.clone()
        ce.dest_type_expr = self.dest_type_expr.clone()

        return ce

    def dbtype(self, converter):
        return self.dest_type_expr.dbtype(converter)


class BinaryExpr(SqlExpr):
    def __init__(self):
        super(BinaryExpr, self).__init__()
        self.expr = None
        self.type = NodeType.Hive_BinaryExpr_EXPR

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return "binary(" + str(self.expr) + ")"


class RatioExpr(SqlExpr):
    def __init__(self):
        super(RatioExpr, self).__init__()
        self.type = NodeType.RatioExpr_EXPR

    def accept0(self, visitor, order):
        pass


# TOP 100
class TopExpr(SqlExpr):
    def __init__(self):
        super(TopExpr, self).__init__()
        self.type = NodeType.TopExpr_EXPR
        self.number = None
        # clickhouse syntax
        self.with_ties = False

    def accept0(self, visitor, order):
        visitor.visit(self)


class LimitExpr(SqlExpr):
    def __init__(self):
        super(LimitExpr, self).__init__()
        self.type = NodeType.LimitExpr_EXPR
        self.limit_columns = Seq(self)
        self.split_type = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        for lc in self.limit_columns:
            lc.accept(visitor)

    def __str__(self):
        if self.split_type == LimitSplitType.COMMA:
            return ",".join(str(c) for c in self.limit_columns)
        elif self.split_type == LimitSplitType.OFFSET:
            return " OFFSET ".join(str(c) for c in self.limit_columns)
        else:
            return str(self.limit_columns[0])


class JoinConstraintExpr(SqlExpr):
    def __init__(self):
        super(JoinConstraintExpr, self).__init__()
        self.type = NodeType.JoinConstraintExpr_EXPR
        # 当前只是一个总的表达式，考虑把所有的条件分割成一条条独立的 and 子句
        self.conditions = Seq(self)
        self.on_using = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        for con in self.conditions:
            con.accept(visitor)

    def __str__(self):
        if self.on_using == JoinConstraintType.USING:
            on_using_info = "USING "
        else:
            on_using_info = "ON "
        return on_using_info + " ".join(str(c) for c in self.conditions)

    def clone(self):
        jce = JoinConstraintExpr()
        for con in self.conditions:
            jce.conditions.append(con.clone())
        jce.on_using = self.on_using

        return jce


class OrderExpr(SqlExpr):
    def __init__(self):
        super(OrderExpr, self).__init__()
        self.type = NodeType.OrderExpr_EXPR
        self.expr = None
        self.order_type = None
        self.null_order_type = None
        self.collate_str = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        if self.order_type == OrderingType.ASC:
            order_type_info = "ASC"
        elif self.order_type == OrderingType.DESC:
            order_type_info = "DESC"
        else:
            order_type_info = ""

        if self.null_order_type == OrderingType.NULL_FIRST:
            null_order_type_info = "NULLS FIRST"
        elif self.null_order_type == OrderingType.NULL_LAST:
            null_order_type_info = "NULLS LAST"
        else:
            null_order_type_info = ""

        if self.collate_str is not None:
            collate_info = "COLLATE " + str(self.collate_str)
        else:
            collate_info = ""

        return str(self.expr) + " " + order_type_info + " " + null_order_type_info + " " + collate_info

    def clone(self):
        oe = OrderExpr()
        oe.expr = self.expr.clone()
        oe.order_type = self.order_type
        oe.null_order_type = self.null_order_type
        oe.collate_str = self.collate_str.clone() if isinstance(self.collate_str, SqlNode) else self.collate_str

        return oe


# 'hello' = 1
class EnumExpr(SqlExpr):
    def __init__(self):
        super(EnumExpr, self).__init__()
        self.type = NodeType.EnumExpr_EXPR
        # STRING_LITERAL
        self.left_str = None
        # numberLiteral
        self.right_num = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return str(self.left_str) + " = " + str(self.right_num)

    def clone(self):
        ee = EnumExpr()
        ee.left_str = self.left_str.clone() if isinstance(self.left_str, SqlNode) else self.left_str
        ee.right_num = self.right_num.clone() if isinstance(self.right_num, SqlNode) else self.right_num

        return ee


class DateExpr(SqlExpr):
    def __init__(self):
        super(DateExpr, self).__init__()
        self.type = NodeType.DateExpr_EXPR
        self.date_info = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return "DATE " + str(self.date_info)

    def clone(self):
        de = DateExpr()
        de.date_info = self.date_info

        return de


# ID UInt32
class TokenDefinitionExpr(SqlExpr):
    def __init__(self):
        super(TokenDefinitionExpr, self).__init__()
        self.type = NodeType.TokenDefinitionExpr_EXPR
        self.token_name = None
        self.type = None

    def accept0(self, visitor, order):
        visitor.visit(self)

    def __str__(self):
        return str(self.token_name) + " " + str(self.type)


class SampleExpr(SqlExpr):
    def __init__(self):
        super(SampleExpr, self).__init__()
        self.type = NodeType.SampleExpr_EXPR
        self.ratio = None
        self.offset = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.ratio.accept(visitor)
        if self.offset is not None:
            self.offset.accept(visitor)

    def __str__(self):
        if self.offset is not None:
            offset_info = "OFFSET " + str(self.offset)
        else:
            offset_info = ""
        return "SAMPLE " + str(self.ratio) + offset_info

    def clone(self):
        se = SampleExpr()
        se.ratio = self.ratio.clone() if isinstance(self.ratio, SqlNode) else self.ratio
        se.offset = self.offset.clone() if isinstance(self.offset, SqlNode) else self.offset

        return se


class ValueTypeDefinitionExpr(SqlExpr):
    def __init__(self):
        super(ValueTypeDefinitionExpr, self).__init__()
        self.type == NodeType.ValueTypeDefinitionExpr_EXPR
        self.value = None
        self.value_type = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.value.accept(visitor)
        self.value_type.accept(visitor)

    def __str__(self):
        return str(self.value) + "::" + str(self.value_type)

    def clone(self):
        vtde = ValueTypeDefinitionExpr()
        vtde.value = self.value.clone() if isinstance(self.value, SqlNode) else self.value
        vtde.value_type = self.value_type

        return vtde
