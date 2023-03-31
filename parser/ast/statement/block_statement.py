from parser.ast.base import SqlStatement, Seq, SqlNode
from parser.ast.type.node_type import NodeType, GroupByType, ArrayJoinType


class SqlBlockStatement(SqlStatement):
    def __init__(self):
        super(SqlBlockStatement, self).__init__()
        self.type = NodeType.BLOCKSTATEMENT


class SelectBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(SelectBlockStatement, self).__init__()
        self.nameExpressions = Seq(self)
        # SQLSetQuantifier type ,eg SQLSetQuantifier.DISTINCT
        self.quantifier = None
        # TopExpr top
        self.top = None
        self.m_symbols = []
        self.type = NodeType.Select_BLOCKSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        for ne in self.nameExpressions:
            ne.accept(visitor)

    def __str__(self):
        if self.quantifier is not None:
            quantifier_info = self.quantifier.name + " "
        else:
            quantifier_info = ""
        return "SELECT " + quantifier_info + ", ".join([str(c) for c in self.nameExpressions if c is not None])

    def clone(self):
        sbs = SelectBlockStatement()
        for item in self.nameExpressions:
            sbs.nameExpressions.append(item.clone())
        sbs.quantifier = self.quantifier
        sbs.top = self.top

        return sbs


class FromBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(FromBlockStatement, self).__init__()
        # SqlFromSource source
        # 可能和m_symbols有部分重叠，为避免干扰原有逻辑，暂时新起一个，后期合并
        self.symbols_states = []
        self.source = None
        self.m_symbols = None
        self.type = NodeType.From_BLOCKSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.source.accept(visitor, order)

    def __str__(self):
        return "FROM %s" % str(self.source)

    def clone(self):
        fbs = FromBlockStatement()
        fbs.source = self.source.clone()

        return fbs


class ArrayJoinBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(ArrayJoinBlockStatement, self).__init__()
        self.type = NodeType.ArrayJoin_BLOCKSTATEMENT
        self.array_join_type = None
        self.array_join_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.array_join_list:
            expr.accept(visitor)

    def __str__(self):
        if self.array_join_type == ArrayJoinType.LEFT_ARRAY_JOIN:
            array_type_info = "LEFT ARRAY JOIN "
        elif self.array_join_type == ArrayJoinType.INNER_ARRAY_JOIN:
            array_type_info = "INNER ARRAY JOIN "
        else:
            array_type_info = "ARRAY JOIN "

        return array_type_info + " , ".join(str(c) for c in self.array_join_list)

    def clone(self):
        ajbs = ArrayJoinBlockStatement()
        ajbs.array_join_type = self.array_join_type
        for item in self.array_join_list:
            ajbs.array_join_list.append(item.clone())

        return ajbs


class WhereBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(WhereBlockStatement, self).__init__()
        self.expr = None
        self.type = NodeType.Where_BLOCKSTATEMENT

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return "WHERE %s" % str(self.expr)

    def clone(self):
        wbs = WhereBlockStatement()
        wbs.expr = self.expr.clone()

        return wbs


class GroupByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(GroupByBlockStatement, self).__init__()
        self.type = NodeType.GroupBy_BLOCKSTATEMENT
        # # 下面两个紧跟" GROUP BY "字段后
        # self.front_cube = None
        # self.front_rollup = None
        self.front_type = None
        # # 下面三个具有" WITH "字段，在整个group语句后
        # self.with_cube = False
        # self.with_rollup = False
        # self.with_totals = False
        self.tail_type = None
        self.group_expressions = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.group_expressions:
            expr.accept(visitor)

    def __str__(self):
        front_info = ""
        if self.front_type == GroupByType.FRONT_CUBE:
            front_info = " CUBE "
        elif self.front_type == GroupByType.FRONT_ROLLUP:
            front_info = " ROLLUP "
        else:
            front_info = " "

        tail_info = ""
        if self.tail_type == GroupByType.TAIL_CUBE:
            tail_info = " WITH CUBE "
        elif self.tail_type == GroupByType.TAIL_ROLLUP:
            tail_info = " WITH ROLLUP "
        elif self.tail_type == GroupByType.TAIL_TOTALS:
            tail_info = " WITH TOTALS "
        else:
            tail_info = " "

        return " GROUP BY " + front_info + "(" + " , ".join(str(c) for c in self.group_expressions) + ")" + tail_info

    def clone(self):
        gbs = GroupByBlockStatement()
        gbs.front_type = self.front_type
        gbs.tail_type = self.tail_type
        for item in self.group_expressions:
            gbs.group_expressions.append(item.clone())

        return gbs


class HavingBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(HavingBlockStatement, self).__init__()
        self.type = NodeType.Having_BLOCKSTATEMENT
        self.expr = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.expr.accept(visitor)

    def __str__(self):
        return "HAVING %s" % str(self.expr)

    def clone(self):
        hbs = HavingBlockStatement()
        hbs.expr = self.expr.clone()

        return hbs


class OrderByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(OrderByBlockStatement, self).__init__()
        self.type = NodeType.OrderBy_BLOCKSTATEMENT
        self.order_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.order_list:
            expr.accept(visitor)

    def __str__(self):
        return "ORDER BY " + ",".join(str(c) for c in self.order_list)

    def clone(self):
        obs = OrderByBlockStatement()
        for item in self.order_list:
            obs.order_list.append(item.clone())

        return obs


# LIMIT [offset_value, ]n BY expressions
# LIMIT n OFFSET offset_value BY expressions
# eg : LIMIT 5 BY domain, device_type
class LimitByBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(LimitByBlockStatement, self).__init__()
        self.type = NodeType.LimitBy_BLOCKSTATEMENT
        self.limit_expr = None
        self.by_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.limit_expr.accept(visitor)
        for expr in self.by_list:
            expr.accept(visitor)

    def __str__(self):
        return "LIMIT " + str(self.limit_expr) + " BY " + ",".join(str(c) for c in self.by_list)

    def clone(self):
        lbs = LimitByBlockStatement()
        lbs.limit_expr = self.limit_expr.clone()
        for item in self.by_list:
            lbs.by_list.append(item.clone())

        return lbs


# LIMIT m OFFSET n
# LIMIT m
class LimitBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(LimitBlockStatement, self).__init__()
        self.type = NodeType.Limit_BLOCKSTATEMENT
        self.limit_expr = None
        self.with_ties = False

    def accept0(self, visitor, order):
        visitor.visit(self)
        self.limit_expr.accept(visitor)

    def __str__(self):
        if self.with_ties is True:
            ties_info = " WITH TIES "
        else:
            ties_info = " "
        return "LIMIT " + str(self.limit_expr) + ties_info

    def clone(self):
        lbs = LimitBlockStatement()
        lbs.limit_expr = self.limit_expr.clone()
        lbs.with_ties = self.with_ties

        return lbs


class TeaLimitBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(TeaLimitBlockStatement, self).__init__()
        self.type = NodeType.TeaLimit_BLOCKSTATEMENT
        self.number = None
        self.group_list = Seq(self)
        self.order_list = Seq(self)
        # Ordering ordering_type
        self.ordering_type = None

    def accept0(self, visitor, order):
        visitor.visit(self)
        for g_expr in self.group_list:
            g_expr.accept(visitor)
        for o_expr in self.order_list:
            o_expr.accept(visitor)

    def __str__(self):
        ordering_info = self.ordering_type.name if self.ordering_type is not None else ""
        return "TEALIMIT " + str(self.number) + " GROUP " + ",".join(str(c) for c in self.group_list) \
               + " ORDER " + ",".join(str(c) for c in self.order_list) + " " + ordering_info

    def clone(self):
        llbs = TeaLimitBlockStatement()
        llbs.number = self.number.clone() if isinstance(self.number, SqlNode) else self.number
        for g_expr in self.group_list:
            llbs.group_list.append(g_expr.clone())
        for o_expr in self.order_list:
            llbs.order_list.append(o_expr.clone())
        llbs.ordering_type = self.ordering_type

        return llbs


class SettingsBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(SettingsBlockStatement, self).__init__()
        self.type = NodeType.Settings_BLOCKSTATEMENT
        self.setting_list = Seq(self)

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.setting_list:
            expr.accept(visitor)

    def __str__(self):
        return "SETTINGS " + ",".join(str(c) for c in self.setting_list)

    def clone(self):
        sbs = SettingsBlockStatement()
        for item in self.setting_list:
            sbs.setting_list.append(item.clone())

        return sbs


class WithBlockStatement(SqlBlockStatement):
    def __init__(self):
        super(WithBlockStatement, self).__init__()
        self.type = NodeType.With_BLOCKSTATEMENT
        self.expr_list = Seq(self)
        self.m_symbols = []

    def accept0(self, visitor, order):
        visitor.visit(self)
        for expr in self.expr_list:
            expr.accept(visitor)

    def __str__(self):
        return "WITH " + ", ".join(str(c) for c in self.expr_list)
