from parser.ast.base import Seq
from parser.ast.statement.block_statement import SqlBlockStatement
from parser.ast.type.node_type import NodeType


class ClusterByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(ClusterByBlockStatement, self).__init__()
        self.type = NodeType.ClusterBy_BLOCKSTATEMENT
        self.cluster_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.cluster_list:
            expr.accept(visitor)

    def __str__(self):
        return "Cluster BY " + ",".join(str(c) for c in self.cluster_list)

    def clone(self):
        cbs = ClusterByBlockStatement()
        for item in self.cluster_list:
            cbs.cluster_list.append(item.clone())

        return cbs


class DistributeByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(DistributeByBlockStatement, self).__init__()
        self.type = NodeType.DistributeBy_BLOCKSTATEMENT
        self.distribute_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.distribute_list:
            expr.accept(visitor)

    def __str__(self):
        return "DISTRIBUTE BY " + ",".join(str(c) for c in self.distribute_list)

    def clone(self):
        dbs = DistributeByBlockStatement()
        for item in self.distribute_list:
            dbs.distribute_list.append(item.clone())

        return dbs


class SortByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(SortByBlockStatement, self).__init__()
        self.type = NodeType.SortBy_BLOCKSTATEMENT
        self.sort_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.sort_list:
            expr.accept(visitor)

    def __str__(self):
        return "SORT BY " + ",".join(str(c) for c in self.sort_list)

    def clone(self):
        sbs = SortByBlockStatement()
        for item in self.sort_list:
            sbs.sort_list.append(item.clone())

        return sbs
