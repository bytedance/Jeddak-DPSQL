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

from antlr4 import CommonTokenStream, DiagnosticErrorListener, InputStream, BailErrorStrategy
from antlr4 import PredictionMode
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from parser.ast.builder.ast_builder import AstBuilder
from parser.ast.dialect.hive.error_listener import SyntaxErrorListener
from parser.ast.dialect.hive.hive_lexer import HiveLexer
from parser.ast.dialect.hive.hive_parser import HiveParser
from parser.ast.dialect.hive.hive_visitor import HiveVisitor
from parser.ast.expr.agg_function_expr import SqlSumFunction, SqlCountFunction, SqlMinFunction, SqlMaxFunction, \
    SqlAvgFunction, SqlVarPopFunction, SqlStdPopFunction, SqlAggFunction
from parser.ast.expr.arithmetic_expr import DivideExpression, NegateExpression, MultiplyExpression, ModuloExpression, \
    AdditionExpression, SubtractionExpression, DivExpression
from parser.ast.expr.base_expr import SelectItem, Identifier, Table, TableFunctionExpr, Column, AllColumns, \
    NestedExpression, Literal, Number, ArrayAccess, TupleAccess, NameExpression, Tuples, Arrays, LambdaExpression, \
    MapExpression
from parser.ast.expr.clickhouse_expr import ExtractFunction, Interval, TimeStampExpression, TrimFunction
from parser.ast.expr.cond_expr import WhenExpression, CaseExpression, IIFFunction, IfExpression, MultiIfExpression, \
    TernaryExpression
from parser.ast.expr.function_expr import CommonFunction, PowerFunction
from parser.ast.expr.logical_bool import LogicalConcat, LogicalEqual, BinaryEqual, LogicalCompare, LogicalIn, \
    LogicalLike, LogicalIsNull, LogicalNot, LogicalAnd, LogicalOr, LogicalBetween, LogicalIsTrue, ExistsQuery
from parser.ast.expr.other import JoinConstraintExpr, SampleExpr, LimitExpr, OrderExpr, TokenDefinitionExpr, \
    CastExpr, DateExpr, ValueTypeDefinitionExpr, EnumExpr, BinaryExpr
from parser.ast.statement.block_statement import WithBlockStatement, SelectBlockStatement, FromBlockStatement, \
    WhereBlockStatement, GroupByBlockStatement, HavingBlockStatement, LimitBlockStatement, OrderByBlockStatement
from parser.ast.statement.hive_block_statement import DistributeByBlockStatement, ClusterByBlockStatement, \
    SortByBlockStatement
from parser.ast.statement.hive_select_statement import HiveSelectStatement
from parser.ast.statement.select_statement import SelectUnionStatement
from parser.ast.tablesource.table_source import SqlTableJoinSource, SqlTableSource, SqlSubquerySource
from parser.ast.type.node_type import UnionType, SQLSetQuantifier, NodeType, JoinType, JoinKind, JoinStrictness, \
    JoinLocality, JoinConstraintType, GroupByType, LimitSplitType, OrderingType, TrimType, AggSumType, LiteralType, \
    OperatorType, LogicalInType, LogicalLikeType, ExprAliasType, TimeIntervalType, DialectType
from parser.ast.type.sql_type import SqlNestedType, SqlEnumType, SqlComplexType, SqlDecimalType, CommonWithParamType, \
    SqlNumberType
from parser.ast.builder.hive_func_switch_builder import hive_switch_func


class HiveAstBuilder(AstBuilder):
    """
        Get the Hive parser, parse sql to ast.

    """

    def get_parser(self, stream):
        lexer = HiveLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = HiveParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL
        lexer._listeners = [SyntaxErrorListener()]
        parser._listeners = [SyntaxErrorListener()]
        parser._errHandler = BailErrorStrategy()
        return parser

    def get_ll_parser(self, stream):
        lexer = HiveLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = HiveParser(stream)
        parser._interp.predictionMode = PredictionMode.LL
        lexer._listeners = [SyntaxErrorListener()]
        parser._listeners = [SyntaxErrorListener()]
        parser._errHandler = BailErrorStrategy()
        return parser

    # debug dedicated
    def get_ll_detect_parser(self, stream):
        lexer = HiveLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = HiveParser(stream)
        parser._interp.predictionMode = PredictionMode.LL_EXACT_AMBIG_DETECTION
        parser._errHandler = DefaultErrorStrategy()
        lexer._listeners = [SyntaxErrorListener(), DiagnosticErrorListener()]
        parser._listeners = [SyntaxErrorListener(), DiagnosticErrorListener()]
        return parser

    def get_expr_ast(self, str):
        istream = InputStream(str)
        parser = self.get_parser(istream)
        ev = ExprVisitor()
        ev_ast = ev.visit(parser.columnsExpr())
        return ev_ast

    def get_query_ast(self, str, metamatcher=None):
        istream = InputStream(str)
        parser = self.get_parser(istream)
        qv = QueryVisitor()
        try:
            queruy_context = parser.query()
        except Exception:
            istream = InputStream(str)
            parser = self.get_ll_parser(istream)
            queruy_context = parser.query()

        query_ast = qv.visit(queruy_context)
        return query_ast

    def get_debug_query_ast(self, str):
        istream = InputStream(str)
        parser = self.get_ll_detect_parser(istream)
        qv = QueryVisitor()
        query_ast = qv.visit(parser.query())
        return query_ast


class QueryVisitor(HiveVisitor):
    def visitQuery(self, ctx: HiveParser.QueryContext):
        return self.visit(ctx.selectUnionStmt())

    def visitSelectUnionStmt(self, ctx: HiveParser.SelectUnionStmtContext):
        selects = [self.visit(ss) for ss in ctx.selectStmtWithParens()]
        select_union_statement = SelectUnionStatement()
        select_union_statement.dialect = DialectType.HIVE
        for select in selects:
            select_union_statement.select_statements.append(select)

        if ctx.stmtUnionFlag(0) is not None:
            union_type = self.visit(ctx.stmtUnionFlag(0))
            select_union_statement.union_type = union_type

        return select_union_statement

    def visitStmtUnionAll(self, ctx: HiveParser.StmtUnionAllContext):
        return UnionType.UNION_ALL

    def visitStmtUnionDistinct(self, ctx: HiveParser.StmtUnionDistinctContext):
        return UnionType.UNION_DISTINCT

    def visitStmtUnion(self, ctx: HiveParser.StmtUnionContext):
        return UnionType.UNION

    def visitSelectStmtWithParens(self, ctx: HiveParser.SelectStmtWithParensContext):
        select_stmt = ctx.selectStmt()
        select_union_stmt = ctx.selectUnionStmt()
        if select_stmt is not None:
            return self.visit(select_stmt)
        elif select_union_stmt is not None:
            return self.visit(select_union_stmt)

    def visitSelectStmt(self, ctx: HiveParser.SelectStmtContext):
        with_clause = ctx.withClause()
        with_block = WithBlockVisitor().visit(with_clause) if with_clause is not None else None

        select_clause = ctx.selectClause()
        select_block = SelectBlockVisitor().visit(select_clause) if select_clause is not None else None

        from_clause = ctx.fromClause()
        from_block = FromBlockVisitor().visit(from_clause) if from_clause is not None else None

        where_clause = ctx.whereClause()
        where_block = WhereBlockVisitor().visit(where_clause) if where_clause is not None else None

        group_by_clause = ctx.groupByClause()
        group_by_block = GroupByBlockVisitor().visit(group_by_clause) if group_by_clause is not None else None

        having_clause = ctx.havingClause()
        having_block = HavingVisitor().visit(having_clause) if having_clause is not None else None

        order_by_clause = ctx.orderByClause()
        order_by_block = OrderByVisitor().visit(order_by_clause) if order_by_clause is not None else None

        cluster_by_clause = ctx.clusterByClause()
        cluster_by_block = PartionByVisitor().visit(cluster_by_clause) if cluster_by_clause is not None else None

        distribute_by_clause = ctx.distributeByClause()
        distribute_by_block = PartionByVisitor().visit(
            distribute_by_clause) if distribute_by_clause is not None else None

        sort_by_clause = ctx.sortByClause()
        sort_by_block = OrderByVisitor().visit(sort_by_clause) if sort_by_clause is not None else None

        limit_clause = ctx.limitClause()
        limit_block = LimitVisitor().visit(limit_clause) if limit_clause is not None else None

        ast = HiveSelectStatement()
        ast.with_block = with_block
        ast.select_block = select_block
        ast.source_block = from_block
        ast.where_block = where_block
        ast.groupBy_block = group_by_block
        ast.having_block = having_block
        ast.orderBy_block = order_by_block
        ast.cluster_block = cluster_by_block
        ast.distribute_block = distribute_by_block
        ast.sort_block = sort_by_block
        ast.limit_block = limit_block

        return ast


class WithBlockVisitor(HiveVisitor):
    def visitWithClause(self, ctx: HiveParser.WithClauseContext):
        column_list = ExprVisitor().visit(ctx.columnExprList())
        with_block = WithBlockStatement()
        for col in column_list:
            with_block.expr_list.append(col)

        return with_block


class SelectBlockVisitor(HiveVisitor):
    def visitSelectClause(self, ctx: HiveParser.SelectClauseContext):
        distinct_flag = ctx.DISTINCT()
        quantifier_type = SQLSetQuantifier.DISTINCT if distinct_flag is not None else None

        top_clause = ctx.topClause()
        top_expr = ExprVisitor().visit(top_clause) if top_clause is not None else None

        column_list = ExprVisitor().visit(ctx.columnExprList())
        select_block = SelectBlockStatement()
        select_block.quantifier = quantifier_type
        select_block.top = top_expr
        for column in column_list:
            if column.type == NodeType.NameExpression_EXPR:
                si = SelectItem()
                si.expr = column.expr
                si.alias = column.alias
                select_block.nameExpressions.append(si)
            else:
                si = SelectItem()
                si.expr = column
                select_block.nameExpressions.append(si)

        return select_block


class FromBlockVisitor(HiveVisitor):
    def visitFromClause(self, ctx: HiveParser.FromClauseContext):
        from_block = FromBlockStatement()
        source_expr = JoinVisitor().visit(ctx.joinExpr())
        from_block.source = source_expr
        return from_block


class WhereBlockVisitor(HiveVisitor):
    def visitWhereExpr(self, ctx: HiveParser.WhereExprContext):
        where_block = WhereBlockStatement()
        condition_expr = ExprVisitor().visit(ctx.columnExpr())
        where_block.expr = condition_expr
        return where_block

    def visitWhereExistsQuery(self, ctx: HiveParser.WhereExistsQueryContext):
        where_block = WhereBlockStatement()
        query = QueryVisitor().visit(ctx.selectStmtWithParens())
        if ctx.NOT() is not None:
            eq = ExistsQuery(True, query)
        else:
            eq = ExistsQuery(False, query)

        where_block.expr = eq
        return where_block


class GroupByBlockVisitor(HiveVisitor):
    def visitGroupFrontCr(self, ctx: HiveParser.GroupFrontCrContext):
        group_by_block = GroupByBlockStatement()
        if ctx.CUBE() is not None:
            group_by_block.front_type = GroupByType.FRONT_CUBE
        else:
            group_by_block.front_type = GroupByType.FRONT_ROLLUP

        if ctx.groupByTailFlag() is not None:
            group_by_block.tail_type = self.visit(ctx.groupByTailFlag())

        column_list = self.visit(ctx.columnExprList())
        for column in column_list:
            group_by_block.group_expressions.append(column)

        return group_by_block

    def visitGroupNoFrontCr(self, ctx: HiveParser.GroupNoFrontCrContext):
        group_by_block = GroupByBlockStatement()
        group_by_block.front_type = GroupByType.Unspecified

        if ctx.groupByTailFlag() is not None:
            group_by_block.tail_type = self.visit(ctx.groupByTailFlag())

        column_list = ExprVisitor().visit(ctx.columnExprList())
        for column in column_list:
            group_by_block.group_expressions.append(column)

        return group_by_block

    def visitGroupWithCube(self, ctx: HiveParser.GroupWithCubeContext):
        return GroupByType.TAIL_CUBE

    def visitGroupWithRollup(self, ctx: HiveParser.GroupWithRollupContext):
        return GroupByType.TAIL_ROLLUP

    def visitGroupWithTotals(self, ctx: HiveParser.GroupWithTotalsContext):
        return GroupByType.TAIL_TOTALS


class HavingVisitor(HiveVisitor):
    def visitHavingClause(self, ctx: HiveParser.HavingClauseContext):
        hbs = HavingBlockStatement()
        hbs.expr = ExprVisitor().visit(ctx.columnExpr())

        return hbs


class LimitVisitor(HiveVisitor):
    def visitLimitClause(self, ctx: HiveParser.LimitClauseContext):
        limit_block = LimitBlockStatement()
        limit_expr = self.visit(ctx.limitExpr())
        limit_block.limit_expr = limit_expr

        if ctx.TIES() is not None:
            limit_block.with_ties = True

        return limit_block

    def visitLimitExpr(self, ctx: HiveParser.LimitExprContext):
        columns = [ExprVisitor().visit(col) for col in ctx.columnExpr()]
        le = LimitExpr()
        for col in columns:
            le.limit_columns.append(col)
        if ctx.COMMA() is not None:
            le.split_type = LimitSplitType.COMMA
        elif ctx.OFFSET() is not None:
            le.split_type = LimitSplitType.OFFSET
        else:
            le.split_type = None

        return le


class OrderByVisitor(HiveVisitor):
    def visitOrderByClause(self, ctx: HiveParser.OrderByClauseContext):
        order_block = OrderByBlockStatement()
        expr_list = self.visit(ctx.orderExprList())
        for expr in expr_list:
            order_block.order_list.append(expr)
        return order_block

    def visitOrderExprList(self, ctx: HiveParser.OrderExprListContext):
        return [self.visit(ne) for ne in ctx.orderExpr()]

    def visitOrderExpr(self, ctx: HiveParser.OrderExprContext):
        order_expr = OrderExpr()
        order_expr.expr = ExprVisitor().visit(ctx.columnExpr())
        if ctx.ASCENDING() or ctx.ASC() is not None:
            order_expr.order_type = OrderingType.ASC
        # No specific differences between DESCENDING and DESC have been found yet, and the same processing method is temporarily followed
        elif ctx.DESCENDING() is not None:
            order_expr.order_type = OrderingType.DESC
        elif ctx.DESC() is not None:
            order_expr.order_type = OrderingType.DESC
        else:
            order_expr.order_type = OrderingType.Unspecified

        if ctx.FIRST() is not None:
            order_expr.null_order_type = OrderingType.NULL_FIRST
        elif ctx.LAST() is not None:
            order_expr.null_order_type = OrderingType.NULL_LAST
        else:
            order_expr.null_order_type = OrderingType.Unspecified

        if ctx.COLLATE() is not None:
            order_expr.collate_str = Identifier(str(ctx.STRING_LITERAL()))

        return order_expr

    def visitSortByClause(self, ctx: HiveParser.SortByClauseContext):
        sort_block = SortByBlockStatement()
        expr_list = self.visit(ctx.orderExprList())
        for expr in expr_list:
            sort_block.sort_list.append(expr)
        return sort_block


class PartionByVisitor(HiveVisitor):
    def visitClusterByClause(self, ctx: HiveParser.ClusterByClauseContext):
        cluster_block = ClusterByBlockStatement()
        expr_list = ExprVisitor().visit(ctx.columnExprList())
        for expr in expr_list:
            cluster_block.cluster_list.append(expr)
        return cluster_block

    def visitDistributeByClause(self, ctx: HiveParser.DistributeByClauseContext):
        distribute_block = DistributeByBlockStatement()
        expr_list = ExprVisitor().visit(ctx.columnExprList())
        for expr in expr_list:
            distribute_block.distribute_list.append(expr)
        return distribute_block


class ExprVisitor(HiveVisitor):
    def visitColumnTypeExprSimple(self, ctx: HiveParser.ColumnTypeExprSimpleContext):
        return self.visit(ctx.identifier())

    def visitColumnTypeExprNested(self, ctx: HiveParser.ColumnTypeExprNestedContext):
        snt = SqlNestedType()

        out_type = self.visit(ctx.identifier(0))
        snt.out_type_name = out_type

        first_tde = TokenDefinitionExpr()
        first_tde.token_name = self.visit(ctx.identifier(1))
        first_tde.type = self.visit(ctx.columnTypeExpr())
        snt.inner_type_seq.append(first_tde)
        for expr in ctx.columnDefinitionExpr():
            snt.inner_type_seq.append(self.visit(expr))

        return snt

    # Usually used for create, insert type statements
    # Enum8('hello' = 1, 'world' = 2)
    def visitColumnTypeExprEnum(self, ctx: HiveParser.ColumnTypeExprEnumContext):
        set = SqlEnumType()
        out_enum_type = self.visit(ctx.identifier())
        set.enum_type = out_enum_type
        for enum_expr in ctx.enumValue():
            set.args.append(self.visit(enum_expr))

        return set

    # Usually used for tuple or array
    # tuple(1, 'a')
    def visitColumnTypeExprComplex(self, ctx: HiveParser.ColumnTypeExprComplexContext):
        sct = SqlComplexType()
        out_type = self.visit(ctx.tupleOrArrayName())
        sct.out_type_name = out_type
        elements = self.visit(ctx.columnExprList())

        for type_expr in elements:
            sct.inner_args.append(type_expr)

        return sct

    def visitColumnTypeDecimal(self, ctx: HiveParser.ColumnTypeDecimalContext):
        type_name = self.visit(ctx.decimaltype)
        type_args = self.visit(ctx.columnExprList())

        decimal_type = SqlDecimalType()
        decimal_type.type_name = type_name

        for arg in type_args:
            decimal_type.args.append(arg)

        return decimal_type

    def visitColumnTypeExprParam(self, ctx: HiveParser.ColumnTypeExprParamContext):
        cwp = CommonWithParamType()
        type_name = self.visit(ctx.identifier())
        type_args = self.visit(ctx.columnExprList())
        cwp.type = type_name
        for arg in type_args:
            cwp.args.append(arg)

        return cwp

    def visitColumnDefinitionExpr(self, ctx: HiveParser.ColumnDefinitionExprContext):
        token_name = self.visit(ctx.identifier())
        type = self.visit(ctx.columnTypeExpr())

        tde = TokenDefinitionExpr()
        tde.token_name = token_name
        tde.type = type

        return tde

    def visitColumnExprList(self, ctx: HiveParser.ColumnExprListContext):
        return [self.visit(ce) for ce in ctx.columnsExpr()]

    def visitColumnExprWhen(self, ctx: HiveParser.ColumnExprWhenContext):
        we = WhenExpression()
        when_expr = self.visit(ctx.columnExpr(0))
        then_expr = self.visit(ctx.columnExpr(1))
        we.when_expr = when_expr
        we.then_expr = then_expr
        return we

    def visitColumnsExprAsterisk(self, ctx: HiveParser.ColumnsExprAsteriskContext):
        table_ident = TableExprVisitor().visit(ctx.tableIdentifier()) if ctx.tableIdentifier() is not None else None
        column = AllColumns()
        if table_ident is not None:
            return Column(table_ident, column)
        else:
            return column

    def visitColumnsExprSubquery(self, ctx: HiveParser.ColumnsExprSubqueryContext):
        query = QueryVisitor().visit(ctx.selectUnionStmt())
        ne = NestedExpression()
        ne.expr = query
        return ne

    def visitCaseExpr(self, ctx: HiveParser.CaseExprContext):
        ce = CaseExpression()
        case_expr = self.visit(ctx.case_expr) if ctx.case_expr is not None else None
        when_exprs = [self.visit(ce) for ce in ctx.columnExprWhen()]
        else_expr = self.visit(ctx.else_expr) if ctx.else_expr is not None else None
        ce.case_expr = case_expr
        for when_expr in when_exprs:
            ce.when_exprs.append(when_expr)
        ce.else_expr = else_expr
        return ce

    def visitColumnExprCase(self, ctx: HiveParser.ColumnExprCaseContext):
        return self.visit(ctx.caseExpr())

    def visitColumnExprCast(self, ctx: HiveParser.ColumnExprCastContext):
        ce = CastExpr()
        src_type_expr = self.visit(ctx.columnExpr())
        dest_type_expr = self.visit(ctx.columnTypeExpr())

        ce.src_type_expr = src_type_expr
        ce.dest_type_expr = dest_type_expr

        return ce

    def visitColumnExprBinaryCast(self, ctx: HiveParser.ColumnExprBinaryCastContext):
        be = BinaryExpr()
        expr = self.visit(ctx.columnExpr())
        be.expr = expr

        return be

    # No specific example found, continue to pay attention
    def visitColumnExprDate(self, ctx: HiveParser.ColumnExprDateContext):
        date_expr = DateExpr()
        date_expr.date_info = ctx.STRING_LITERAL().getText()

        return date_expr

    def visitColumnExprExtract(self, ctx: HiveParser.ColumnExprExtractContext):
        ee = ExtractFunction()
        part = self.visit(ctx.interval())
        date = self.visit(ctx.columnExpr())

        ee.part = part
        ee.date = date

        return ee

    def visitColumnExprInterval(self, ctx: HiveParser.ColumnExprIntervalContext):
        interval = Interval()
        value = self.visit(ctx.columnExpr())
        value_type = self.visit(ctx.interval())

        interval.value = value
        interval.value_type = value_type

        return interval

    def visitColumnExprSubstring(self, ctx: HiveParser.ColumnExprSubstringContext):
        func_name = Identifier("substring")
        arg_list = [self.visit(c) for c in ctx.columnExpr()]

        cf = CommonFunction(func_name)
        cf.args = arg_list
        return cf

    def visitColumnExprTimestamp(self, ctx: HiveParser.ColumnExprTimestampContext):
        te = TimeStampExpression()
        te.str = ctx.STRING_LITERAL().getText()

        return te

    def visitColumnExprTrim(self, ctx: HiveParser.ColumnExprTrimContext):
        tf = TrimFunction()
        if ctx.BOTH() is not None:
            trim_type = TrimType.BOTH
        elif ctx.LEADING() is not None:
            trim_type = TrimType.LEADING
        else:
            trim_type = TrimType.TRAILING

        trim_str = ctx.STRING_LITERAL()
        input_str = self.visit(ctx.columnExpr())

        tf.trim_type = trim_type
        tf.trim_str = trim_str
        tf.input_str = input_str

        return tf

    # sum case
    def visitColumnExprSumCaseFunction(self, ctx: HiveParser.ColumnExprSumCaseFunctionContext):
        case_expr = self.visit(ctx.caseExpr())
        sum_func = SqlSumFunction()
        sum_func.args.append(case_expr)
        if case_expr.type == NodeType.CaseExpression_EXPR:
            sum_func.args_type = AggSumType.CASE_EXPR
        return sum_func

    # todo to be further subdivided
    def visitColumnExprAggFunction(self, ctx: HiveParser.ColumnExprAggFunctionContext):
        func_name = str(self.visit(ctx.aggregateFunctionName())).upper()
        if func_name == "COUNT":
            agg_function = SqlCountFunction()
        elif func_name == "MIN":
            agg_function = SqlMinFunction()
        elif func_name == "MAX":
            agg_function = SqlMaxFunction()
        elif func_name == "SUM":
            agg_function = SqlSumFunction()
        elif func_name == "AVG":
            agg_function = SqlAvgFunction()
        elif func_name == "VAR_POP" or func_name == "VARIANCE":
            agg_function = SqlVarPopFunction()
            agg_function.func_name = "var_pop"
        elif func_name == "STDDEV_POP":
            agg_function = SqlStdPopFunction()
            agg_function.func_name = "stddev_pop"
        else:
            agg_function = SqlAggFunction()

        arg_list = self.visit(ctx.columnArgList()) if ctx.columnArgList() is not None else None
        if arg_list is not None:
            for arg in arg_list:
                agg_function.args.append(arg)
        if ctx.DISTINCT() is not None:
            agg_function.flag_type = SQLSetQuantifier.DISTINCT
        if ctx.ALL() is not None:
            agg_function.flag_type = SQLSetQuantifier.ALL

        return agg_function

    def visitColumnExprIfExpr(self, ctx: HiveParser.ColumnExprIfExprContext):
        if ctx.IIF() is not None:
            ie = IIFFunction()
        else:
            ie = IfExpression()

        ie.cond = self.visit(ctx.cond)
        ie.then_expr = self.visit(ctx.trueExpr)
        ie.else_expr = self.visit(ctx.falseExpr)
        return ie

    def visitColumnExprMultiIfExpr(self, ctx: HiveParser.ColumnExprMultiIfExprContext):
        arg_list = self.visit(ctx.columnArgList())
        mie = MultiIfExpression()
        for arg in arg_list:
            mie.args.append(arg)
        return mie

    def visitColumnExprPowFunction(self, ctx: HiveParser.ColumnExprPowFunctionContext):
        pf = PowerFunction()
        pf.expr = self.visit(ctx.columnExpr())

        if ctx.numberLiteral() is not None:
            num = self.visit(ctx.numberLiteral())
        else:
            num = Literal()
            num.type = LiteralType.NULL_LITERAL

        pf.number = num

        return pf

    def visitColumnExprFunction(self, ctx: HiveParser.ColumnExprFunctionContext):
        func_name = self.visit(ctx.identifier())
        column_expr_list = self.visit(ctx.columnExprList()) if ctx.columnExprList() is not None else None
        distinct_flag = SQLSetQuantifier.DISTINCT if ctx.DISTINCT() is not None else None
        arg_list = self.visit(ctx.columnArgList()) if ctx.columnArgList() is not None else None

        hive_func = hive_switch_func(func_name, column_expr_list, arg_list, distinct_flag)
        if hive_func is not None:
            return hive_func

        cf = CommonFunction(str(func_name))
        if column_expr_list is not None:
            for column in column_expr_list:
                cf.column_list.append(column)
        if arg_list is not None:
            for arg in arg_list:
                cf.args.append(arg)
        cf.distinct_flag = distinct_flag
        return cf

    def visitColumnQuoteExpr(self, ctx: HiveParser.ColumnQuoteExprContext):
        me = MapExpression()
        map_name = self.visit(ctx.columnExpr())
        map_key = ctx.STRING_LITERAL()
        me.map_name = map_name
        me.map_key = str(map_key)
        return me

    def visitNumberLiteral(self, ctx: HiveParser.NumberLiteralContext):
        # plus_expr = ctx.PLUS()
        # dash_expr = ctx.DASH()
        float_expr = ctx.floatingLiteral()
        octal_expr = ctx.OCTAL_LITERAL()
        # decimal_expr = ctx.DECIMAL_LITERAL()
        hex_decimal_expr = ctx.HEXADECIMAL_LITERAL()
        inf_expr = ctx.INF()
        nan_sql_expr = ctx.NAN_SQL()

        text = ctx.getText()
        if inf_expr is not None:
            num = Number("inf")
            num.type = SqlNumberType.INF
        elif nan_sql_expr is not None:
            num = Number("nan")
            num.type = SqlNumberType.NAN
        elif float_expr is not None:
            if text.startswith('0x') or text.startswith('-0x'):
                num = Number(float.fromhex(text))
            else:
                num = Number(float(text))
            num.type = SqlNumberType.Float64
        else:
            if octal_expr is not None:
                num = Number(int(text, 8))
            elif hex_decimal_expr is not None:
                num = Number(int(text, 16))
            else:
                num = Number(int(text))
            num.type = SqlNumberType.Int64

        literal = Literal(num)
        literal.type = LiteralType.NUM_LITERAL
        return literal

    def visitStringliteral(self, ctx: HiveParser.StringliteralContext):
        literal = Literal(str(ctx.STRING_LITERAL()))
        literal.type = LiteralType.STRING_LITERAL
        return literal

    def visitNullliteral(self, ctx: HiveParser.NullliteralContext):
        literal = Literal()
        literal.type = LiteralType.NULL_LITERAL
        return literal

    def visitColumnExprArrayAccess(self, ctx: HiveParser.ColumnExprArrayAccessContext):
        array = self.visit(ctx.columnExpr(0))
        key = self.visit(ctx.columnExpr(1))
        if str(key).isnumeric():
            aa = ArrayAccess()
            aa.array = array
            aa.key = int(str(key))
            return aa
        else:
            me = MapExpression()
            me.dialect_type = DialectType.HIVE
            me.map_name = str(array)
            me.map_key = str(key)
            return me

    def visitColumnExprTupleAccess(self, ctx: HiveParser.ColumnExprTupleAccessContext):
        ta = TupleAccess()
        tuple_name = self.visit(ctx.columnExpr())
        num = Number(int(str(ctx.DECIMAL_LITERAL())))

        ta.tuple = tuple_name
        ta.number = num

        return ta

    def visitColumnExprNegate(self, ctx: HiveParser.ColumnExprNegateContext):
        ne = NegateExpression()
        ne.expr = self.visit(ctx.columnExpr())

        return ne

    def visitColumnExprPrecedence1(self, ctx: HiveParser.ColumnExprPrecedence1Context):
        col0 = self.visit(ctx.columnExpr(0))
        col1 = self.visit(ctx.columnExpr(1))

        if ctx.ASTERISK() is not None:
            me = MultiplyExpression(col0, col1)
            return me
        elif ctx.SLASH() is not None:
            de = DivideExpression(col0, col1)
            return de
        elif ctx.DIV() is not None:
            ddiv = DivExpression(col0, col1)
            return ddiv
        else:
            me = ModuloExpression(col0, col1)
            return me

    def visitColumnExprPrecedence2(self, ctx: HiveParser.ColumnExprPrecedence2Context):
        col0 = self.visit(ctx.columnExpr(0))
        col1 = self.visit(ctx.columnExpr(1))

        if ctx.PLUS() is not None:
            ae = AdditionExpression(col0, col1)
            return ae
        elif ctx.DASH() is not None:
            se = SubtractionExpression(col0, col1)
            return se
        else:
            lc = LogicalConcat(col0, col1)
            return lc

    def visitColumnExprPrecedence3(self, ctx: HiveParser.ColumnExprPrecedence3Context):
        col0 = self.visit(ctx.columnExpr(0))
        col1 = self.visit(ctx.columnExpr(1))

        if ctx.EQ_DOUBLE() is not None:
            le = LogicalEqual(col0, col1, OperatorType.EQ_DOUBLE)
            return le
        elif ctx.EQUAL_NS() is not None:
            le = LogicalEqual(col0, col1, OperatorType.HIVE_EQ_NS)
            return le
        elif ctx.EQ_SINGLE() is not None:
            be = BinaryEqual(col0, col1)
            return be
        # != and <> are temporarily combined as !=
        elif ctx.NOT_EQ() is not None:
            le = LogicalEqual(col0, col1, OperatorType.NOT_EQ_1)
            return le
        elif ctx.LE() is not None:
            lc = LogicalCompare(col0, col1, OperatorType.LE)
            return lc
        elif ctx.GE() is not None:
            lc = LogicalCompare(col0, col1, OperatorType.GE)
            return lc
        elif ctx.LT() is not None:
            lc = LogicalCompare(col0, col1, OperatorType.LT)
            return lc
        elif ctx.GT() is not None:
            lc = LogicalCompare(col0, col1, OperatorType.GT)
            return lc
        elif ctx.IN() is not None:
            if ctx.GLOBAL() is not None:
                if ctx.NOT() is not None:
                    flag_type = LogicalInType.GLOBAL_NOT_IN
                else:
                    flag_type = LogicalInType.GLOBAL_IN
            else:
                if ctx.NOT() is not None:
                    flag_type = LogicalInType.NOT_IN
                else:
                    flag_type = LogicalInType.IN

            li = LogicalIn(col0, col1, flag_type)
            return li
        else:
            if ctx.NOT() is not None:
                if ctx.LIKE() is not None:
                    flag_type = LogicalLikeType.NOT_LIKE
                else:
                    flag_type = LogicalLikeType.NOT_ILIKE
            else:
                if ctx.LIKE() is not None:
                    flag_type = LogicalLikeType.LIKE
                else:
                    flag_type = LogicalLikeType.ILIKE
            ll = LogicalLike(col0, col1, flag_type)
            return ll

    def visitColumnExprIsNull(self, ctx: HiveParser.ColumnExprIsNullContext):
        lin = LogicalIsNull()
        lin.expr = self.visit(ctx.columnExpr())
        if ctx.NOT() is not None:
            lin.notFlag = True
        else:
            lin.notFlag = False

        return lin

    def visitColumnExprIsTrue(self, ctx: HiveParser.ColumnExprIsTrueContext):
        lit = LogicalIsTrue()
        lit.expr = self.visit(ctx.columnExpr())
        if ctx.NOT() is not None:
            lit.not_flag = True
        else:
            lit.not_flag = False

        if ctx.JSON_TRUE() is not None:
            lit.value_flag = True
        else:
            lit.value_flag = False

    def visitColumnExprNot(self, ctx: HiveParser.ColumnExprNotContext):
        col = self.visit(ctx.columnExpr())
        ln = LogicalNot(col)
        return ln

    def visitColumnExprAnd(self, ctx: HiveParser.ColumnExprAndContext):
        col0 = self.visit(ctx.columnExpr(0))
        col1 = self.visit(ctx.columnExpr(1))
        la = LogicalAnd(col0, col1)
        return la

    def visitColumnExprOr(self, ctx: HiveParser.ColumnExprOrContext):
        col0 = self.visit(ctx.columnExpr(0))
        col1 = self.visit(ctx.columnExpr(1))
        lo = LogicalOr(col0, col1)
        return lo

    def visitColumnExprBetween(self, ctx: HiveParser.ColumnExprBetweenContext):
        lb = LogicalBetween()
        lb.value = self.visit(ctx.columnExpr(0))
        lb.lower_bound = self.visit(ctx.columnExpr(1))
        lb.upper_bound = self.visit(ctx.columnExpr(2))
        if ctx.NOT() is not None:
            lb.not_flag = True
        else:
            lb.not_flag = False

        return lb

    def visitColumnExprTernaryOp(self, ctx: HiveParser.ColumnExprTernaryOpContext):
        te = TernaryExpression()
        te.cond_expr = self.visit(ctx.columnExpr(0))
        te.then_expr = self.visit(ctx.columnExpr(1))
        te.else_expr = self.visit(ctx.columnExpr(2))

        return te

    def visitColumnExprAlias(self, ctx: HiveParser.ColumnExprAliasContext):
        exp = self.visit(ctx.columnExpr())
        ne = NameExpression()
        ne.expr = exp

        if ctx.alias() is not None:
            ne.alias = self.visit(ctx.alias())
            ne.alias_type = ExprAliasType.alias
        else:
            ne.alias = self.visit(ctx.identifier())
            ne.alias_type = ExprAliasType.AS

        return ne

    def visitColumnExprAliasSubquery(self, ctx: HiveParser.ColumnExprAliasSubqueryContext):
        ident = self.visit(ctx.identifier())
        query = QueryVisitor().visit(ctx.selectUnionStmt())
        ne = NameExpression()
        ne.expr = ident

        nne = NestedExpression()
        nne.expr = query
        ne.alias = nne

        return ne

    def visitColumnExprAsterisk(self, ctx: HiveParser.ColumnExprAsteriskContext):
        table_ident = TableExprVisitor().visit(ctx.tableIdentifier()) if ctx.tableIdentifier() is not None else None
        column = AllColumns()
        if table_ident is not None:
            return Column(table_ident, column)
        else:
            return column

    def visitColumnExprSubquery(self, ctx: HiveParser.ColumnExprSubqueryContext):
        query = QueryVisitor().visit(ctx.selectUnionStmt())
        ne = NestedExpression()
        ne.expr = query
        return ne

    def visitColumnExprParens(self, ctx: HiveParser.ColumnExprParensContext):
        expr = self.visit(ctx.columnExpr())
        ne = NestedExpression()
        ne.expr = expr
        return ne

    def visitColumnExprTuple(self, ctx: HiveParser.ColumnExprTupleContext):
        ttuple = Tuples()

        if ctx.columnExprList() is not None:
            column_list = self.visit(ctx.columnExprList())
            for col in column_list:
                ttuple.args.append(col)

        return ttuple

    def visitColumnExprArray(self, ctx: HiveParser.ColumnExprArrayContext):
        array = Arrays()

        if ctx.columnExprList() is not None:
            column_list = self.visit(ctx.columnExprList())
            for col in column_list:
                array.args.append(col)

        return array

    def visitColumnExprIdentifier(self, ctx: HiveParser.ColumnExprIdentifierContext):
        return TableExprVisitor().visit(ctx)

    def visitColumnTypeDefinition(self, ctx: HiveParser.ColumnTypeDefinitionContext):
        value = self.visit(ctx.columnExpr())
        type = self.visit(ctx.columnTypeExpr())

        vtde = ValueTypeDefinitionExpr()
        vtde.value = value
        vtde.value_type = type

        return vtde

    def visitColumnArgList(self, ctx: HiveParser.ColumnArgListContext):
        return [self.visit(ne) for ne in ctx.columnArgExpr()]

    def visitColumnLambdaExpr(self, ctx: HiveParser.ColumnLambdaExprContext):
        le = LambdaExpression()
        for ident in ctx.identifier():
            le.left_list.append(self.visit(ident))
        le.right = self.visit(ctx.columnExpr())
        return le

    def visitNestedIdentifier(self, ctx: HiveParser.NestedIdentifierContext):
        first_ident = self.visit(ctx.identifier(0))
        second_expr = ctx.identifier(1)
        second_ident = self.visit(second_expr) if second_expr is not None else None
        return first_ident if second_ident is None else Identifier(first_ident.text + "." + second_ident.text)

    def visitInterval(self, ctx: HiveParser.IntervalContext):
        inter = ctx.getText().upper()
        for interval in TimeIntervalType:
            if inter == interval.name:
                return interval

        return TimeIntervalType.Unspecified

    def visitAggregateFunctionName(self, ctx: HiveParser.AggregateFunctionNameContext):
        ident = Identifier(ctx.getText().upper())
        return ident

    def visitKeyword(self, ctx: HiveParser.KeywordContext):
        ident = Identifier(ctx.getText())
        return ident

    def visitKeywordForAlias(self, ctx: HiveParser.KeywordForAliasContext):
        ident = Identifier(ctx.getText())
        return ident

    def visitAlias(self, ctx: HiveParser.AliasContext):
        if ctx.IDENTIFIER() is not None:
            return Identifier(ctx.getText())
        else:
            return self.visit(ctx.keywordForAlias())

    def visitIdentifier(self, ctx: HiveParser.IdentifierContext):
        ident = Identifier(ctx.getText())
        return ident

    def visitEnumValue(self, ctx: HiveParser.EnumValueContext):
        enum_expr = EnumExpr()
        enum_expr.left = Identifier(str(ctx.STRING_LITERAL()))
        enum_expr.right_num = self.visit(ctx.numberLiteral())

        return enum_expr

    def visitDecimalTypeName(self, ctx: HiveParser.DecimalTypeNameContext):
        return ctx.getText()

    def visitTupleOrArrayName(self, ctx: HiveParser.TupleOrArrayNameContext):
        return ctx.getText()


class JoinVisitor(HiveVisitor):
    def visitJoinExprOp(self, ctx: HiveParser.JoinExprOpContext):
        left_join_expr = self.visit(ctx.joinExpr(0))
        right_join_expr = self.visit(ctx.joinExpr(1))

        if ctx.joinOp() is not None:
            join_type = self.visit(ctx.joinOp())
        else:
            join_type = JoinType()
            # JOIN without specified type implies INNER
            join_type.kind = JoinKind.Inner
            join_type.strictness = JoinStrictness.Unspecified
        if ctx.LOCAL() is not None:
            join_type.locality = JoinLocality.Local
        elif ctx.GLOBAL() is not None:
            join_type.locality = JoinLocality.Global
        else:
            join_type.locality = JoinLocality.Unspecified

        join_condition = self.visit(ctx.joinConstraintClause())

        sql_source = SqlTableJoinSource()
        sql_source.left_table = left_join_expr
        sql_source.right_table = right_join_expr
        sql_source.join_type = join_type
        sql_source.join_condition = join_condition

        return sql_source

    def visitJoinExprCrossOp(self, ctx: HiveParser.JoinExprCrossOpContext):
        left_join_expr = self.visit(ctx.joinExpr(0))
        right_join_expr = self.visit(ctx.joinExpr(1))
        join_type = self.visit(ctx.joinOpCross())

        sql_source = SqlTableJoinSource()
        sql_source.left_table = left_join_expr
        sql_source.right_table = right_join_expr
        sql_source.join_type = join_type

        return sql_source

    def visitJoinExprTable(self, ctx: HiveParser.JoinExprTableContext):
        table_source = TableExprVisitor().visit(ctx.tableExpr())
        if ctx.sampleClause() is not None:
            table_source.sample = self.visit(ctx.sampleClause())
        return table_source

    def visitJoinExprParens(self, ctx: HiveParser.JoinExprParensContext):
        return self.visit(ctx.joinExpr())

    def visitJoinOpInner1(self, ctx: HiveParser.JoinOpInner1Context):
        join_type = JoinType()
        join_type.kind = JoinKind.Inner
        if ctx.ALL() is not None:
            join_type.strictness = JoinStrictness.All
        elif ctx.ANY() is not None:
            join_type.strictness = JoinStrictness.Any
        elif ctx.ASOF() is not None:
            join_type.strictness = JoinStrictness.Asof
        else:
            join_type.strictness = JoinStrictness.Unspecified

        return join_type

    def visitJoinOpInner2(self, ctx: HiveParser.JoinOpInner2Context):
        return self.visitJoinOpInner1(ctx)

    def visitJoinOpInner3(self, ctx: HiveParser.JoinOpInner3Context):
        return self.visitJoinOpInner1(ctx)

    def visitJoinOpLeftRight1(self, ctx: HiveParser.JoinOpLeftRight1Context):
        join_type = JoinType()
        if ctx.ALL() is not None:
            join_type.strictness = JoinStrictness.All
        elif ctx.ANY() is not None:
            join_type.strictness = JoinStrictness.Any
        elif ctx.ASOF() is not None:
            join_type.strictness = JoinStrictness.Asof
        elif ctx.SEMI() is not None:
            join_type.strictness = JoinStrictness.Semi
        elif ctx.ANTI() is not None:
            join_type.strictness = JoinStrictness.Anti
        else:
            join_type.strictness = JoinStrictness.Unspecified

        if ctx.LEFT() is not None:
            join_type.kind = JoinKind.Left
        else:
            join_type.kind = JoinKind.Right

        return join_type

    def visitJoinOpLeftRight2(self, ctx: HiveParser.JoinOpLeftRight2Context):
        return self.visitJoinOpLeftRight1(ctx)

    def visitJoinOpFull1(self, ctx: HiveParser.JoinOpFull1Context):
        join_type = JoinType()
        join_type.kind = JoinKind.Full
        if ctx.ALL() is not None:
            join_type.strictness = JoinStrictness.All
        elif ctx.ANY() is not None:
            join_type.strictness = JoinStrictness.Any
        else:
            join_type.strictness = JoinStrictness.Unspecified

        return join_type

    def visitJoinOpFull2(self, ctx: HiveParser.JoinOpFull2Context):
        return self.visitJoinOpFull1(ctx)

    def visitJoinOpCross(self, ctx: HiveParser.JoinOpCrossContext):
        join_type = JoinType()
        join_type.kind = JoinKind.Cross
        join_type.strictness = JoinStrictness.Unspecified

        if ctx.GLOBAL() is not None:
            join_type.locality = JoinLocality.Global
        elif ctx.LOCAL() is not None:
            join_type.locality = JoinLocality.Local
        else:
            join_type.locality = JoinLocality.Unspecified

        return join_type

    def visitJoinConstraintClause(self, ctx: HiveParser.JoinConstraintClauseContext):
        conditions = ExprVisitor().visit(ctx.columnExprList())
        constraint = JoinConstraintExpr()
        # 后续考虑把condition分割后再放入
        for condition in conditions:
            constraint.conditions.append(condition)
        if ctx.USING() is not None:
            constraint.on_using = JoinConstraintType.USING
        else:
            constraint.on_using = JoinConstraintType.ON

        return constraint

    def visitSampleClause(self, ctx: HiveParser.SampleClauseContext):
        ratio = self.visit(ctx.ratioExpr(0))
        if ctx.OFFSET() is not None:
            offset = self.visit(ctx.ratioExpr(1))
        else:
            offset = None

        se = SampleExpr()
        se.ratio = ratio
        se.offset = offset

        return se

    def visitRatioExpr(self, ctx: HiveParser.RatioExprContext):
        num1 = ExprVisitor().visit(ctx.numberLiteral(0))
        if ctx.SLASH() is not None:
            num2 = ExprVisitor().visit(ctx.numberLiteral(1))
            num = DivideExpression(num1, num2)
        else:
            num = num1

        return num


class TableExprVisitor(HiveVisitor):

    def visitColumnIdentifier(self, ctx: HiveParser.ColumnIdentifierContext):
        table_expr = ctx.tableIdentifier()
        table_ident = self.visit(table_expr) if table_expr is not None else None
        nested_expr = ctx.nestedIdentifier()
        nested_ident = ExprVisitor().visit(nested_expr)

        if table_ident is not None:
            return Identifier(str(table_ident) + "." + nested_ident.text)
        else:
            return nested_ident

    def visitTableIdentifier(self, ctx: HiveParser.TableIdentifierContext):
        database_expr = ctx.databaseIdentifier()
        database_ident = self.visit(database_expr) if database_expr is not None else None
        table_ident = ExprVisitor().visit(ctx.identifier())

        table_expr = Table(database_ident, table_ident)
        table_source = SqlTableSource(table_expr)

        return table_source

    def visitTableFunctionExpr(self, ctx: HiveParser.TableFunctionExprContext):
        tfe = TableFunctionExpr()
        tfe.name = ExprVisitor().visit(ctx.identifier())
        args = self.visit(ctx.tableArgList())
        for arg in args:
            tfe.table_args.append(arg)

        return tfe

    def visitTableExprSubquery(self, ctx: HiveParser.TableExprSubqueryContext):
        query = QueryVisitor().visit(ctx.selectUnionStmt())
        sql_source = SqlSubquerySource(query)
        return sql_source

    def visitTableExprAlias(self, ctx: HiveParser.TableExprAliasContext):
        table = self.visit(ctx.tableExpr())
        if ctx.alias() is not None:
            alias = ExprVisitor().visit(ctx.alias())
        else:
            alias = ExprVisitor().visit(ctx.identifier())
        table.alias = alias

        return table

    def visitTableArgList(self, ctx: HiveParser.TableArgListContext):
        return [self.visit(ta) for ta in ctx.tableArgExpr()]

    def visitTableArgExpr(self, ctx: HiveParser.TableArgExprContext):
        if ctx.tableIdentifier() is not None:
            return self.visit(ctx.tableIdentifier())
        elif ctx.tableFunctionExpr() is not None:
            return self.visit(ctx.tableFunctionExpr())
        else:
            return ExprVisitor().visit(ctx.literal())

    def visitDatabaseIdentifier(self, ctx: HiveParser.DatabaseIdentifierContext):
        ident = ExprVisitor().visit(ctx.identifier())
        return ident
