from parser.ast.statement.select_statement import SelectStatement
from parser.ast.type.node_type import DialectType, NodeType
from parser.ast.visitor.tree_visitor import VisitorOrder


class HiveSelectStatement(SelectStatement):
    def __init__(self):
        super(HiveSelectStatement, self).__init__()
        self.with_block = None
        self.cluster_block = None
        self.distribute_block = None
        self.sort_block = None
        self.dialect = DialectType.HIVE
        self.type = NodeType.Hive_SQLSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        if order == VisitorOrder.FORWARD:
            if self.with_block is not None:
                self.with_block.accept(visitor)
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
        elif order == VisitorOrder.SYMBOLLOADING:
            if self.source_block is not None:
                self.source_block.accept(visitor)
            if self.select_block is not None:
                self.select_block.accept(visitor)
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
            if self.with_block is not None:
                self.with_block.accept(visitor)
