from parser.ast.base import SqlStatement, Seq
from parser.ast.type.node_type import NodeType, DialectType, UnionType

# base select statement
from parser.ast.visitor.tree_visitor import VisitorOrder


# 在clickhouse的规则文件中只发现了union all操作符，所以暂时不启用SqlUnionSource
# add: 在官方文档中发现union有三种形态：UNION/UNION ALL/UNION DISTINCT
class SelectUnionStatement(SqlStatement):
    def __init__(self):
        super(SelectUnionStatement, self).__init__()
        self.select_statements = Seq(self)
        self.type = NodeType.Union_SQLSTATEMENT
        self.union_type = None
        self.dialect = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        for query in self.select_statements:
            query.accept(visitor, order)

    def __str__(self):
        if self.union_type == UnionType.UNION_DISTINCT:
            union_info = " UNION DISTINCT "
        elif self.union_type == UnionType.UNION:
            union_info = " UNION "
        else:
            union_info = " UNION ALL  "

        return union_info.join([str(c) for c in self.select_statements if c is not None])

    def clone(self):
        sus = SelectUnionStatement()
        for item in self.select_statements:
            sus.select_statements.append(item.clone())
        sus.union_type = self.union_type

        return sus


class SelectStatement(SqlStatement):
    def __init__(self):
        super(SelectStatement, self).__init__()
        self.select_block = None
        self.source_block = None
        self.where_block = None
        self.groupBy_block = None
        self.having_block = None
        self.orderBy_block = None
        self.limit_block = None
        self.symbols = []
        self.dialect = None
        self.type = NodeType.Common_SQLSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        if order == VisitorOrder.FORWARD:
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
        else:
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor)
            if self.select_block is not None:
                self.select_block.accept(visitor)

    def clone(self):
        bss = SelectStatement()
        if self.select_block is not None:
            bss.select_block = self.select_block.clone()
        if self.source_block is not None:
            bss.source_block = self.source_block.clone()
        if self.where_block is not None:
            bss.where_block = self.where_block.clone()
        if self.groupBy_block is not None:
            bss.groupBy_block = self.groupBy_block.clone()
        if self.having_block is not None:
            bss.having_block = self.having_block.clone()
        if self.orderBy_block is not None:
            bss.orderBy_block = self.orderBy_block.clone()
        if self.limit_block is not None:
            bss.limit_block = self.limit_block.clone()

        return bss


class ClickHouseSelectStatement(SelectStatement):
    def __init__(self):
        super(ClickHouseSelectStatement, self).__init__()
        self.with_block = None
        self.array_join_block = None
        self.prewhere_block = None
        self.setting_block = None
        self.format_block = None
        self.dialect = DialectType.CLICKHOUSE
        self.type = NodeType.Clickhouse_SQLSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        if order == VisitorOrder.FORWARD:
            if self.with_block is not None:
                self.with_block.accept(visitor)
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor)
            if self.array_join_block is not None:
                self.array_join_block.accept(visitor)
            if self.prewhere_block is not None:
                self.prewhere_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
            if self.setting_block is not None:
                self.setting_block.accept(visitor)
            if self.format_block is not None:
                self.format_block.accept(visitor)
        else:
            if self.format_block is not None:
                self.format_block.accept(visitor)
            if self.setting_block is not None:
                self.setting_block.accept(visitor)
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.prewhere_block is not None:
                self.prewhere_block.accept(visitor)
            if self.array_join_block is not None:
                self.array_join_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor)
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.with_block is not None:
                self.with_block.accept(visitor)

    def clone(self):
        bss = ClickHouseSelectStatement()
        if self.with_block is not None:
            bss.with_block = self.with_block.clone()
        if self.select_block is not None:
            bss.select_block = self.select_block.clone()
        if self.source_block is not None:
            bss.source_block = self.source_block.clone()
        if self.array_join_block is not None:
            bss.array_join_block = self.array_join_block.clone()
        if self.prewhere_block is not None:
            bss.prewhere_block = self.prewhere_block.clone()
        if self.where_block is not None:
            bss.where_block = self.where_block.clone()
        if self.groupBy_block is not None:
            bss.groupBy_block = self.groupBy_block.clone()
        if self.having_block is not None:
            bss.having_block = self.having_block.clone()
        if self.orderBy_block is not None:
            bss.orderBy_block = self.orderBy_block.clone()
        if self.limit_block is not None:
            bss.limit_block = self.limit_block.clone()
        if self.setting_block is not None:
            bss.setting_block = self.setting_block.clone()

        return bss


class ByteClickHouseSelectStatement(ClickHouseSelectStatement):
    def __init__(self):
        super(ByteClickHouseSelectStatement, self).__init__()
        self.tealimit_block = None
        self.type = NodeType.Byte_Clickhouse_SQLSTATEMENT

    # 用于正向遍历
    def accept0(self, visitor, order):
        visitor.visit(self)
        if order == VisitorOrder.FORWARD:
            if self.with_block is not None:
                self.with_block.accept(visitor)
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor, order)
            if self.array_join_block is not None:
                self.array_join_block.accept(visitor)
            if self.prewhere_block is not None:
                self.prewhere_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
            if self.tealimit_block is not None:
                self.tealimit_block.accept(visitor)
            if self.setting_block is not None:
                self.setting_block.accept(visitor)
        elif order == VisitorOrder.BACKWARD:
            if self.setting_block is not None:
                self.setting_block.accept(visitor)
            if self.tealimit_block is not None:
                self.tealimit_block.accept(visitor)
            if self.limit_block is not None:
                self.limit_block.accept(visitor)
            if self.orderBy_block is not None:
                self.orderBy_block.accept(visitor)
            if self.having_block is not None:
                self.having_block.accept(visitor)
            if self.groupBy_block is not None:
                self.groupBy_block.accept(visitor)
            if self.where_block is not None:
                self.where_block.accept(visitor)
            if self.prewhere_block is not None:
                self.prewhere_block.accept(visitor)
            if self.array_join_block is not None:
                self.array_join_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor, order)
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.with_block is not None:
                self.with_block.accept(visitor)
        elif order == VisitorOrder.SIMPLESEARCH:
            if self.select_block is not None:
                self.select_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor, order)
        else:
            if self.with_block is not None:
                self.with_block.accept(visitor)
            if self.source_block is not None:
                self.source_block.accept(visitor, order)
            if self.select_block is not None:
                self.select_block.accept(visitor)

    def clone(self):
        bss = ByteClickHouseSelectStatement()
        if self.with_block is not None:
            bss.with_block = self.with_block.clone()
        if self.select_block is not None:
            bss.select_block = self.select_block.clone()
        if self.source_block is not None:
            bss.source_block = self.source_block.clone()
        if self.array_join_block is not None:
            bss.array_join_block = self.array_join_block.clone()
        if self.prewhere_block is not None:
            bss.prewhere_block = self.prewhere_block.clone()
        if self.where_block is not None:
            bss.where_block = self.where_block.clone()
        if self.groupBy_block is not None:
            bss.groupBy_block = self.groupBy_block.clone()
        if self.having_block is not None:
            bss.having_block = self.having_block.clone()
        if self.orderBy_block is not None:
            bss.orderBy_block = self.orderBy_block.clone()
        if self.limit_block is not None:
            bss.limit_block = self.limit_block.clone()
        if self.tealimit_block is not None:
            bss.tealimit_block = self.tealimit_block.clone()
        if self.setting_block is not None:
            bss.setting_block = self.setting_block.clone()

        return bss
