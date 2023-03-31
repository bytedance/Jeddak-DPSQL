from parser.ast.base import SqlNode
from parser.ast.type.node_type import NodeType


class SqlSource(SqlNode):
    def __init__(self):
        super(SqlSource, self).__init__()
        self.type = NodeType.SqlSource
        self.alias = None
        self.sample = None

    def __str__(self):
        info = ""
        if self.alias is not None:
            info = info + " " + str(self.alias)

        if self.sample is not None:
            info = info + " " + str(self.sample)

        return info


class SqlTableSource(SqlSource):
    """
        Mainly consider a single table.

    """

    def __init__(self, table_expr):
        super(SqlTableSource, self).__init__()
        self.table_expr = table_expr
        self.type = NodeType.SqlTableSource

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.table_expr.accept(visitor)

    def __str__(self):
        return str(self.table_expr) + super(SqlTableSource, self).__str__()

    def clone(self):
        sts = SqlTableSource(self.table_expr.clone())
        return sts


class SqlTableJoinSource(SqlSource):
    def __init__(self):
        super(SqlTableJoinSource, self).__init__()
        # SqlSource left
        self.left_table = None
        # SqlSource right
        self.right_table = None
        # JoinType join_type
        self.join_type = None
        self.join_condition = None
        self.type = NodeType.SqlTableJoinSource

    def accept0(self, visitor, order):
        self.left_table.accept(visitor, order)
        # visitor.visit(self)
        self.right_table.accept(visitor, order)
        if self.join_condition is not None:
            self.join_condition.accept(visitor, order)
        visitor.visit(self)

    def __str__(self):
        if self.join_condition is not None:
            join_condition_info = str(self.join_condition)
        else:
            join_condition_info = ""
        return str(self.left_table) + str(self.join_type) + str(self.right_table) + " " + join_condition_info + super(
            SqlTableJoinSource, self).__str__()

    def clone(self):
        source = SqlTableJoinSource()
        source.left_table = self.left_table.clone()
        source.right_table = self.right_table.clone()
        source.join_type = self.join_type
        source.join_condition = self.join_condition.clone() if self.join_condition is not None else None

        return source


# 暂时由SelectUnionStatement代替，在考虑SqlUnionSource的使用方式
class SqlUnionSource(SqlSource):
    def __init__(self):
        super(SqlUnionSource, self).__init__()
        self.left_statement = None
        self.union_type = None
        self.right_statement = None
        self.type = NodeType.SqlUnionSource

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.left_statement.accept(visitor)
        self.right_statement.accept(visitor)


class SqlSubquerySource(SqlSource):
    def __init__(self, query):
        super(SqlSubquerySource, self).__init__()
        # SelectStatement select_query
        self.select_query = query
        self.type = NodeType.SqlSubquerySource

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.select_query.accept(visitor, order)

    def __str__(self):
        if self.alias is not None:
            return "(" + str(self.select_query) + ") " + str(self.alias)
        else:
            return "(" + str(self.select_query) + ")"

    def clone(self):
        source = SqlSubquerySource(self.select_query.clone())

        return source


# https://clickhouse.tech/docs/zh/sql-reference/statements/select/array-join/
# clickhouse 语法独有
class SqlArrayJoinSource(SqlSource):
    def __init__(self):
        super(SqlArrayJoinSource, self).__init__()
        self.type = NodeType.SqlArrayJoinSource

    def accept0(self, visitor, order):
        visitor.visit(self)


class FusionMergeSource(SqlSource):
    def __init__(self, db, first_table, second_table, split_column, split_info, range1, range2, alias):
        super(FusionMergeSource, self).__init__()
        self.type = NodeType.SqlFusionMergeSource
        self.db = db
        self.first_table = first_table
        self.second_table = second_table
        self.split_column = split_column
        self.split_info = split_info
        self.range1 = range1
        self.range2 = range2
        self.alias = alias

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.first_table.accept(visitor)
        self.second_table.accept(visitor)
        self.split_info.accept(visitor)

    def __str__(self):
        if self.alias is not None:
            alias_info = str(self.alias)
        else:
            alias_info = ""

        return "fusionMerge(" + str(self.db) + ", " + str(self.first_table) + ", " + str(
            self.second_table) + ", " + str(self.split_column) + ", " + str(self.split_info) + ", " + str(
            self.range1) + ", " + str(self.range2) + ") " + alias_info

    def clone(self):
        source = FusionMergeSource(self.db.clone(), self.first_table.clone(),
                                   self.second_table.clone(), self.split_column.clone,
                                   self.split_info.clone(), self.range1.clone(),
                                   self.range2.clone(), None)

        if self.alias is not None:
            source.alias = self.alias.clone()

        return source
