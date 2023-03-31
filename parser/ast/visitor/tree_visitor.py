from enum import Enum

from parser.ast.type.node_type import NodeType


class VisitorOrder(Enum):
    FORWARD = 1
    BACKWARD = 2
    SYMBOLLOADING = 3
    SIMPLESEARCH = 4


class TreeVisitor(object):

    def preVisit(self, node):
        # sql select statement
        if node.type == NodeType.Union_SQLSTATEMENT:
            return self.preVisitUnionSelectStatement(node)
        elif node.type == NodeType.Common_SQLSTATEMENT:
            return self.preVisitSelectStatement(node)
        elif node.type == NodeType.Clickhouse_SQLSTATEMENT:
            return self.preVisitClickHouseSelectStatement(node)
        elif node.type == NodeType.Byte_Clickhouse_SQLSTATEMENT:
            return self.preVisitByteClickHouseSelectStatement(node)
        elif node.type == NodeType.Hive_SQLSTATEMENT:
            return self.preVisitHiveSelectStatement(node)

        # sql block statement
        elif node.type == NodeType.Select_BLOCKSTATEMENT:
            return self.preVisitSelectBlockStatement(node)
        elif node.type == NodeType.From_BLOCKSTATEMENT:
            return self.preVisitFromBlockStatement(node)
        elif node.type == NodeType.ArrayJoin_BLOCKSTATEMENT:
            return self.preVisitArrayJoinBlockStatement(node)
        elif node.type == NodeType.Where_BLOCKSTATEMENT:
            return self.preVisitWhereBlockStatement(node)
        elif node.type == NodeType.GroupBy_BLOCKSTATEMENT:
            return self.preVisitGroupByBlockStatement(node)
        elif node.type == NodeType.Having_BLOCKSTATEMENT:
            return self.preVisitHavingBlockStatement(node)
        elif node.type == NodeType.OrderBy_BLOCKSTATEMENT:
            return self.preVisitOrderByBlockStatement(node)
        elif node.type == NodeType.LimitBy_BLOCKSTATEMENT:
            return self.preVisitLimitByBlockStatement(node)
        elif node.type == NodeType.Limit_BLOCKSTATEMENT:
            return self.preVisitLimitBlockStatement(node)
        elif node.type == NodeType.TeaLimit_BLOCKSTATEMENT:
            return self.preVisitTeaLimitBlockStatement(node)
        elif node.type == NodeType.With_BLOCKSTATEMENT:
            return self.preVisitWithBlockStatement(node)
        elif node.type == NodeType.PreWhere_BLOCKSTATEMENT:
            return self.preVisitPrewhereBlockStatement(node)
        elif node.type == NodeType.Settings_BLOCKSTATEMENT:
            return self.preVisitSettingsBlockStatement(node)
        elif node.type == NodeType.Sample_BLOCKSTATEMENT:
            return self.preVisitSampleBlockStatement(node)
        elif node.type == NodeType.ClusterBy_BLOCKSTATEMENT:
            return self.preVisitClusterByBlockStatement(node)
        elif node.type == NodeType.DistributeBy_BLOCKSTATEMENT:
            return self.preVisitDistributeByBlockStatement(node)
        elif node.type == NodeType.SortBy_BLOCKSTATEMENT:
            return self.preVisitSortByBlockStatement(node)

        # sql base expr
        elif node.type == NodeType.Literal_EXPR:
            return self.preVisitLiteral(node)
        elif node.type == NodeType.Identifier_EXPR:
            return self.preVisitIdentifier(node)
        elif node.type == NodeType.Number_EXPR:
            return self.preVisitNumber(node)
        elif node.type == NodeType.Column_EXPR:
            return self.preVisitColumn(node)
        elif node.type == NodeType.AllColumns_EXPR:
            return self.preVisitAllColumns(node)
        elif node.type == NodeType.ArrayAccess_EXPR:
            return self.preVisitArrayAccess(node)
        elif node.type == NodeType.TupleAccess_EXPR:
            return self.preVisitTupleAccess(node)
        elif node.type == NodeType.Arrays_EXPR:
            return self.preVisitArrays(node)
        elif node.type == NodeType.Tuples_EXPR:
            return self.preVisitTuples(node)
        elif node.type == NodeType.MapExpression_EXPR:
            return self.preVisitMapExpression(node)
        elif node.type == NodeType.Table_EXPR:
            return self.preVisitTable(node)
        elif node.type == NodeType.TableFunction_EXPR:
            return self.preVisitTableFunctionExpr(node)
        elif node.type == NodeType.Maps_EXPR:
            return self.preVisitMaps(node)

        # sql complex expr
        elif node.type == NodeType.NameExpression_EXPR:
            return self.preVisitNameExpression(node)
        elif node.type == NodeType.NestedExpression_EXPR:
            return self.preVisitNestedExpression(node)
        elif node.type == NodeType.Interval_EXPR:
            return self.preVisitInterval(node)
        elif node.type == NodeType.LambdaExpression_EXPR:
            return self.preVisitLambdaExpression(node)
        elif node.type == NodeType.CastExpr_EXPR:
            return self.preVisitCastExpr(node)
        elif node.type == NodeType.RatioExpr_EXPR:
            return self.preVisitRatioExpr(node)
        elif node.type == NodeType.TopExpr_EXPR:
            return self.preVisitTopExpr(node)
        elif node.type == NodeType.LimitExpr_EXPR:
            return self.preVisitLimitExpr(node)
        elif node.type == NodeType.JoinConstraintExpr_EXPR:
            return self.preVisitJoinConstraintExpr(node)
        elif node.type == NodeType.OrderExpr_EXPR:
            return self.preVisitOrderExpr(node)
        elif node.type == NodeType.EnumExpr_EXPR:
            return self.preVisitEnumExpr(node)
        elif node.type == NodeType.DateExpr_EXPR:
            return self.preVisitDateExpr(node)
        elif node.type == NodeType.TokenDefinitionExpr_EXPR:
            return self.preVisitTokenDefinitionExpr(node)
        elif node.type == NodeType.SelectItem_EXPR:
            return self.preVisitSelectItem(node)
        elif node.type == NodeType.SampleExpr_EXPR:
            return self.preVisitSampleExpr(node)
        elif node.type == NodeType.ValueTypeDefinitionExpr_EXPR:
            return self.preVisitValueTypeDefinitionExpr(node)
        elif node.type == NodeType.FormatExpr_EXPR:
            return self.preVisitFormatExpr(node)
        elif node.type == NodeType.Hive_BinaryExpr_EXPR:
            return self.preVisitBinaryExpr(node)

        # sql agg functiong
        elif node.type == NodeType.SqlAggFunction_EXPR:
            return self.preVisitSqlAggFunction(node)
        elif node.type == NodeType.SqlCountFunction_EXPR:
            return self.preVisitSqlCountFunction(node)
        elif node.type == NodeType.SqlMinFunction_EXPR:
            return self.preVisitSqlMinFunction(node)
        elif node.type == NodeType.SqlMaxFunction_EXPR:
            return self.preVisitSqlMaxFunction(node)
        elif node.type == NodeType.SqlSumFunction_EXPR:
            return self.preVisitSqlSumFunction(node)
        elif node.type == NodeType.SqlAvgFunction_EXPR:
            return self.preVisitSqlAvgFunction(node)
        elif node.type == NodeType.SqlVarPopFunction_EXPR:
            return self.preVisitSqlVarPopFunction(node)
        elif node.type == NodeType.SqlVarSampFunction_EXPR:
            return self.preVisitSqlVarSampFunction(node)
        elif node.type == NodeType.SqlStdPopFunction_EXPR:
            return self.preVisitSqlStdPopFunction(node)
        elif node.type == NodeType.SqlStdSampFunction_EXPR:
            return self.preVisitSqlStdSampFunction(node)

        # sql arithmetic
        elif node.type == NodeType.NegateExpression_EXPR:
            return self.preVisitNegateExpression(node)
        elif node.type == NodeType.MultiplyExpression_EXPR:
            return self.preVisitMultiplyExpression(node)
        elif node.type == NodeType.DivideExpression_EXPR:
            return self.preVisitDivideExpression(node)
        elif node.type == NodeType.ModuloExpression_EXPR:
            return self.preVisitModuloExpression(node)
        elif node.type == NodeType.AdditionExpression_EXPR:
            return self.preVisitAdditionExpression(node)
        elif node.type == NodeType.SubtractionExpression_EXPR:
            return self.preVisitSubtractionExpression(node)
        elif node.type == NodeType.DivExpression_EXPR:
            return self.preVisitDivExpression(node)

        # sql cond expression
        elif node.type == NodeType.IfExpression_EXPR:
            return self.preVisitIfExpression(node)
        elif node.type == NodeType.IIFFunction_EXPR:
            return self.preVisitIIFFunction(node)
        elif node.type == NodeType.MultiIfExpression_EXPR:
            return self.preVisitMultiIfExpression(node)
        elif node.type == NodeType.CaseExpression_EXPR:
            return self.preVisitCaseExpression(node)
        elif node.type == NodeType.WhenExpression_EXPR:
            return self.preVisitWhenExpression(node)
        elif node.type == NodeType.TernaryExpression_EXPR:
            return self.preVisitTernaryExpression(node)
        elif node.type == NodeType.Hive_NVLExpression_EXPR:
            return self.preVisitNvlFuncExpressio(node)
        elif node.type == NodeType.CoalesceFunction_EXPR:
            return self.preVisitCoalesceFuncExpression(node)
        elif node.type == NodeType.Hive_NullIfFunction_EXPR:
            return self.preVisitNullIfFuncExpression(node)
        elif node.type == NodeType.Hive_AssertTrueFunction_EXPR:
            return self.preVisitAssertTrueFuncExpression(node)

        # sql function
        elif node.type == NodeType.CommonFunction_EXPR:
            return self.preVisitCommonFunction(node)
        elif node.type == NodeType.ExtractFunction_EXPR:
            return self.preVisitExtractFunction(node)
        elif node.type == NodeType.MathFunction_EXPR:
            return self.preVisitMathFunction(node)
        elif node.type == NodeType.BareFunction_EXPR:
            return self.preVisitBareFunction(node)
        elif node.type == NodeType.RoundFunction_EXPR:
            return self.preVisitRoundFunction(node)
        elif node.type == NodeType.PowerFunction_EXPR:
            return self.preVisitPowerFunction(node)
        elif node.type == NodeType.QuantilesFunction_EXPR:
            return self.preVisitQuantilesFunction(node)
        elif node.type == NodeType.Quantiles2Function_EXPR:
            return self.preVisitQuantiles2Function(node)
        elif node.type == NodeType.Quantiles3Function_EXPR:
            return self.preVisitQuantiles3Function(node)
        elif node.type == NodeType.ClickHouseCommonFunction_EXPR:
            return self.preVisitClickHouseCommonFunction(node)
        elif node.type == NodeType.TrimFunction_EXPR:
            return self.preVisitTrimFunction(node)
        elif node.type == NodeType.ColumnsFunction_EXPR:
            return self.preVisitColumnsFunction(node)
        elif node.type == NodeType.ToTypeNameFunction_EXPR:
            return self.preVisitToTypeNameFunction(node)

        # sql logical bool
        elif node.type == NodeType.BinaryEqual_EXPR:
            return self.preVisitBinaryEqual(node)
        elif node.type == NodeType.LogicalEqual_EXPR:
            return self.preVisitLogicalEqual(node)
        elif node.type == NodeType.LogicalNot_EXPR:
            return self.preVisitLogicalNot(node)
        elif node.type == NodeType.LogicalAnd_EXPR:
            return self.preVisitLogicalAnd(node)
        elif node.type == NodeType.LogicalOr_EXPR:
            return self.preVisitLogicalOr(node)
        elif node.type == NodeType.LogicalConcat_EXPR:
            return self.preVisitLogicalConcat(node)
        elif node.type == NodeType.LogicalIsNull_EXPR:
            return self.preVisitLogicalIsNull(node)
        elif node.type == NodeType.LogicalCompare_EXPR:
            return self.preVisitLogicalCompare(node)
        elif node.type == NodeType.LogicalIn_EXPR:
            return self.preVisitLogicalIn(node)
        elif node.type == NodeType.LogicalLike_EXPR:
            return self.preVisitLogicalLike(node)
        elif node.type == NodeType.LogicalBetween_EXPR:
            return self.preVisitLogicalBetween(node)
        elif node.type == NodeType.LogicalIsTrue_EXPR:
            return self.preVisitLogicalIsTrue(node)
        elif node.type == NodeType.LogicalExistsQuery_EXPR:
            return self.preVisitExistsQuery(node)

        # sql table source
        elif node.type == NodeType.SqlTableSource:
            return self.preVisitSqlTableSource(node)
        elif node.type == NodeType.SqlTableJoinSource:
            return self.preVisitSqlTableJoinSource(node)
        elif node.type == NodeType.SqlUnionSource:
            return self.preVisitSqlUnionSource(node)
        elif node.type == NodeType.SqlSubquerySource:
            return self.preVisitSqlSubquerySource(node)
        elif node.type == NodeType.SqlArrayJoinSource:
            return self.preVisitSqlArrayJoinSource(node)
        elif node.type == NodeType.SqlFusionMergeSource:
            return self.preVisitFusionMergeSource(node)

    def visit(self, node):
        # sql select statement
        if node.type == NodeType.Union_SQLSTATEMENT:
            return self.visitUnionSelectStatement(node)
        elif node.type == NodeType.Common_SQLSTATEMENT:
            return self.visitSelectStatement(node)
        elif node.type == NodeType.Clickhouse_SQLSTATEMENT:
            return self.visitClickHouseSelectStatement(node)
        elif node.type == NodeType.Byte_Clickhouse_SQLSTATEMENT:
            return self.visitByteClickHouseSelectStatement(node)
        elif node.type == NodeType.Hive_SQLSTATEMENT:
            return self.visitHiveSelectStatement(node)

        # sql block statement
        elif node.type == NodeType.Select_BLOCKSTATEMENT:
            return self.visitSelectBlockStatement(node)
        elif node.type == NodeType.From_BLOCKSTATEMENT:
            return self.visitFromBlockStatement(node)
        elif node.type == NodeType.ArrayJoin_BLOCKSTATEMENT:
            return self.visitArrayJoinBlockStatement(node)
        elif node.type == NodeType.Where_BLOCKSTATEMENT:
            return self.visitWhereBlockStatement(node)
        elif node.type == NodeType.GroupBy_BLOCKSTATEMENT:
            return self.visitGroupByBlockStatement(node)
        elif node.type == NodeType.Having_BLOCKSTATEMENT:
            return self.visitHavingBlockStatement(node)
        elif node.type == NodeType.OrderBy_BLOCKSTATEMENT:
            return self.visitOrderByBlockStatement(node)
        elif node.type == NodeType.LimitBy_BLOCKSTATEMENT:
            return self.visitLimitByBlockStatement(node)
        elif node.type == NodeType.Limit_BLOCKSTATEMENT:
            return self.visitLimitBlockStatement(node)
        elif node.type == NodeType.TeaLimit_BLOCKSTATEMENT:
            return self.visitTeaLimitBlockStatement(node)
        elif node.type == NodeType.With_BLOCKSTATEMENT:
            return self.visitWithBlockStatement(node)
        elif node.type == NodeType.PreWhere_BLOCKSTATEMENT:
            return self.visitPrewhereBlockStatement(node)
        elif node.type == NodeType.Settings_BLOCKSTATEMENT:
            return self.visitSettingsBlockStatement(node)
        elif node.type == NodeType.Sample_BLOCKSTATEMENT:
            return self.visitSampleBlockStatement(node)
        elif node.type == NodeType.ClusterBy_BLOCKSTATEMENT:
            return self.visitClusterByBlockStatement(node)
        elif node.type == NodeType.DistributeBy_BLOCKSTATEMENT:
            return self.visitDistributeByBlockStatement(node)
        elif node.type == NodeType.SortBy_BLOCKSTATEMENT:
            return self.visitSortByBlockStatement(node)

        # sql base expr
        elif node.type == NodeType.Literal_EXPR:
            return self.visitLiteral(node)
        elif node.type == NodeType.Identifier_EXPR:
            return self.visitIdentifier(node)
        elif node.type == NodeType.Number_EXPR:
            return self.visitNumber(node)
        elif node.type == NodeType.Column_EXPR:
            return self.visitColumn(node)
        elif node.type == NodeType.AllColumns_EXPR:
            return self.visitAllColumns(node)
        elif node.type == NodeType.ArrayAccess_EXPR:
            return self.visitArrayAccess(node)
        elif node.type == NodeType.TupleAccess_EXPR:
            return self.visitTupleAccess(node)
        elif node.type == NodeType.Arrays_EXPR:
            return self.visitArrays(node)
        elif node.type == NodeType.Tuples_EXPR:
            return self.visitTuples(node)
        elif node.type == NodeType.MapExpression_EXPR:
            return self.visitMapExpression(node)
        elif node.type == NodeType.Table_EXPR:
            return self.visitTable(node)
        elif node.type == NodeType.TableFunction_EXPR:
            return self.visitTableFunctionExpr(node)
        elif node.type == NodeType.Maps_EXPR:
            return self.visitMaps(node)

        # sql complex expr
        elif node.type == NodeType.NameExpression_EXPR:
            return self.visitNameExpression(node)
        elif node.type == NodeType.NestedExpression_EXPR:
            return self.visitNestedExpression(node)
        elif node.type == NodeType.Interval_EXPR:
            return self.visitInterval(node)
        elif node.type == NodeType.LambdaExpression_EXPR:
            return self.visitLambdaExpression(node)
        elif node.type == NodeType.CastExpr_EXPR:
            return self.visitCastExpr(node)
        elif node.type == NodeType.RatioExpr_EXPR:
            return self.visitRatioExpr(node)
        elif node.type == NodeType.TopExpr_EXPR:
            return self.visitTopExpr(node)
        elif node.type == NodeType.LimitExpr_EXPR:
            return self.visitLimitExpr(node)
        elif node.type == NodeType.JoinConstraintExpr_EXPR:
            return self.visitJoinConstraintExpr(node)
        elif node.type == NodeType.OrderExpr_EXPR:
            return self.visitOrderExpr(node)
        elif node.type == NodeType.EnumExpr_EXPR:
            return self.visitEnumExpr(node)
        elif node.type == NodeType.DateExpr_EXPR:
            return self.visitDateExpr(node)
        elif node.type == NodeType.TokenDefinitionExpr_EXPR:
            return self.visitTokenDefinitionExpr(node)
        elif node.type == NodeType.SelectItem_EXPR:
            return self.visitSelectItem(node)
        elif node.type == NodeType.SampleExpr_EXPR:
            return self.visitSampleExpr(node)
        elif node.type == NodeType.ValueTypeDefinitionExpr_EXPR:
            return self.visitValueTypeDefinitionExpr(node)
        elif node.type == NodeType.FormatExpr_EXPR:
            return self.visitFormatExpr(node)
        elif node.type == NodeType.Hive_BinaryExpr_EXPR:
            return self.visitBinaryExpr(node)

        # sql agg functiong
        elif node.type == NodeType.SqlAggFunction_EXPR:
            return self.visitSqlAggFunction(node)
        elif node.type == NodeType.SqlCountFunction_EXPR:
            return self.visitSqlCountFunction(node)
        elif node.type == NodeType.SqlMinFunction_EXPR:
            return self.visitSqlMinFunction(node)
        elif node.type == NodeType.SqlMaxFunction_EXPR:
            return self.visitSqlMaxFunction(node)
        elif node.type == NodeType.SqlSumFunction_EXPR:
            return self.visitSqlSumFunction(node)
        elif node.type == NodeType.SqlAvgFunction_EXPR:
            return self.visitSqlAvgFunction(node)
        elif node.type == NodeType.SqlVarPopFunction_EXPR:
            return self.visitSqlVarPopFunction(node)
        elif node.type == NodeType.SqlVarSampFunction_EXPR:
            return self.visitSqlVarSampFunction(node)
        elif node.type == NodeType.SqlStdPopFunction_EXPR:
            return self.visitSqlStdPopFunction(node)
        elif node.type == NodeType.SqlStdSampFunction_EXPR:
            return self.visitSqlStdSampFunction(node)

        # sql arithmetic
        elif node.type == NodeType.NegateExpression_EXPR:
            return self.visitNegateExpression(node)
        elif node.type == NodeType.MultiplyExpression_EXPR:
            return self.visitMultiplyExpression(node)
        elif node.type == NodeType.DivideExpression_EXPR:
            return self.visitDivideExpression(node)
        elif node.type == NodeType.ModuloExpression_EXPR:
            return self.visitModuloExpression(node)
        elif node.type == NodeType.AdditionExpression_EXPR:
            return self.visitAdditionExpression(node)
        elif node.type == NodeType.SubtractionExpression_EXPR:
            return self.visitSubtractionExpression(node)
        elif node.type == NodeType.DivExpression_EXPR:
            return self.visitDivExpression(node)

        # sql cond expression
        elif node.type == NodeType.IfExpression_EXPR:
            return self.visitIfExpression(node)
        elif node.type == NodeType.IIFFunction_EXPR:
            return self.visitIIFFunction(node)
        elif node.type == NodeType.MultiIfExpression_EXPR:
            return self.visitMultiIfExpression(node)
        elif node.type == NodeType.CaseExpression_EXPR:
            return self.visitCaseExpression(node)
        elif node.type == NodeType.WhenExpression_EXPR:
            return self.visitWhenExpression(node)
        elif node.type == NodeType.TernaryExpression_EXPR:
            return self.visitTernaryExpression(node)
        elif node.type == NodeType.Hive_NVLExpression_EXPR:
            return self.visitNvlFuncExpressio(node)
        elif node.type == NodeType.CoalesceFunction_EXPR:
            return self.visitCoalesceFuncExpression(node)
        elif node.type == NodeType.Hive_NullIfFunction_EXPR:
            return self.visitNullIfFuncExpression(node)
        elif node.type == NodeType.Hive_AssertTrueFunction_EXPR:
            return self.visitAssertTrueFuncExpression(node)

        # sql function
        elif node.type == NodeType.CommonFunction_EXPR:
            return self.visitCommonFunction(node)
        elif node.type == NodeType.ExtractFunction_EXPR:
            return self.visitExtractFunction(node)
        elif node.type == NodeType.MathFunction_EXPR:
            return self.visitMathFunction(node)
        elif node.type == NodeType.BareFunction_EXPR:
            return self.visitBareFunction(node)
        elif node.type == NodeType.RoundFunction_EXPR:
            return self.visitRoundFunction(node)
        elif node.type == NodeType.PowerFunction_EXPR:
            return self.visitPowerFunction(node)
        elif node.type == NodeType.QuantilesFunction_EXPR:
            return self.visitQuantilesFunction(node)
        elif node.type == NodeType.Quantiles2Function_EXPR:
            return self.visitQuantiles2Function(node)
        elif node.type == NodeType.Quantiles3Function_EXPR:
            return self.visitQuantiles3Function(node)
        elif node.type == NodeType.ClickHouseCommonFunction_EXPR:
            return self.visitClickHouseCommonFunction(node)
        elif node.type == NodeType.TrimFunction_EXPR:
            return self.visitTrimFunction(node)
        elif node.type == NodeType.ColumnsFunction_EXPR:
            return self.visitColumnsFunction(node)
        elif node.type == NodeType.ToTypeNameFunction_EXPR:
            return self.visitToTypeNameFunction(node)

        # sql logical bool
        elif node.type == NodeType.BinaryEqual_EXPR:
            return self.visitBinaryEqual(node)
        elif node.type == NodeType.LogicalEqual_EXPR:
            return self.visitLogicalEqual(node)
        elif node.type == NodeType.LogicalNot_EXPR:
            return self.visitLogicalNot(node)
        elif node.type == NodeType.LogicalAnd_EXPR:
            return self.visitLogicalAnd(node)
        elif node.type == NodeType.LogicalOr_EXPR:
            return self.visitLogicalOr(node)
        elif node.type == NodeType.LogicalConcat_EXPR:
            return self.visitLogicalConcat(node)
        elif node.type == NodeType.LogicalIsNull_EXPR:
            return self.visitLogicalIsNull(node)
        elif node.type == NodeType.LogicalCompare_EXPR:
            return self.visitLogicalCompare(node)
        elif node.type == NodeType.LogicalIn_EXPR:
            return self.visitLogicalIn(node)
        elif node.type == NodeType.LogicalLike_EXPR:
            return self.visitLogicalLike(node)
        elif node.type == NodeType.LogicalBetween_EXPR:
            return self.visitLogicalBetween(node)
        elif node.type == NodeType.LogicalIsTrue_EXPR:
            return self.visitLogicalIsTrue(node)
        elif node.type == NodeType.LogicalExistsQuery_EXPR:
            return self.visitExistsQuery(node)

        # sql table source
        elif node.type == NodeType.SqlTableSource:
            return self.visitSqlTableSource(node)
        elif node.type == NodeType.SqlTableJoinSource:
            return self.visitSqlTableJoinSource(node)
        elif node.type == NodeType.SqlUnionSource:
            return self.visitSqlUnionSource(node)
        elif node.type == NodeType.SqlSubquerySource:
            return self.visitSqlSubquerySource(node)
        elif node.type == NodeType.SqlArrayJoinSource:
            return self.visitSqlArrayJoinSource(node)
        elif node.type == NodeType.SqlFusionMergeSource:
            return self.visitFusionMergeSource(node)

    def postVisit(self, node):
        # sql select statement
        if node.type == NodeType.Union_SQLSTATEMENT:
            return self.postVisitUnionSelectStatement(node)
        elif node.type == NodeType.Common_SQLSTATEMENT:
            return self.postVisitSelectStatement(node)
        elif node.type == NodeType.Clickhouse_SQLSTATEMENT:
            return self.postVisitClickHouseSelectStatement(node)
        elif node.type == NodeType.Byte_Clickhouse_SQLSTATEMENT:
            return self.postVisitByteClickHouseSelectStatement(node)
        elif node.type == NodeType.Hive_SQLSTATEMENT:
            return self.postVisitHiveSelectStatement(node)

        # sql block statement
        elif node.type == NodeType.Select_BLOCKSTATEMENT:
            return self.postVisitSelectBlockStatement(node)
        elif node.type == NodeType.From_BLOCKSTATEMENT:
            return self.postVisitFromBlockStatement(node)
        elif node.type == NodeType.ArrayJoin_BLOCKSTATEMENT:
            return self.postVisitArrayJoinBlockStatement(node)
        elif node.type == NodeType.Where_BLOCKSTATEMENT:
            return self.postVisitWhereBlockStatement(node)
        elif node.type == NodeType.GroupBy_BLOCKSTATEMENT:
            return self.postVisitGroupByBlockStatement(node)
        elif node.type == NodeType.Having_BLOCKSTATEMENT:
            return self.postVisitHavingBlockStatement(node)
        elif node.type == NodeType.OrderBy_BLOCKSTATEMENT:
            return self.postVisitOrderByBlockStatement(node)
        elif node.type == NodeType.LimitBy_BLOCKSTATEMENT:
            return self.postVisitLimitByBlockStatement(node)
        elif node.type == NodeType.Limit_BLOCKSTATEMENT:
            return self.postVisitLimitBlockStatement(node)
        elif node.type == NodeType.TeaLimit_BLOCKSTATEMENT:
            return self.postVisitTeaLimitBlockStatement(node)
        elif node.type == NodeType.With_BLOCKSTATEMENT:
            return self.postVisitWithBlockStatement(node)
        elif node.type == NodeType.PreWhere_BLOCKSTATEMENT:
            return self.postVisitPrewhereBlockStatement(node)
        elif node.type == NodeType.Settings_BLOCKSTATEMENT:
            return self.postVisitSettingsBlockStatement(node)
        elif node.type == NodeType.Sample_BLOCKSTATEMENT:
            return self.postVisitSampleBlockStatement(node)
        elif node.type == NodeType.ClusterBy_BLOCKSTATEMENT:
            return self.postVisitClusterByBlockStatement(node)
        elif node.type == NodeType.DistributeBy_BLOCKSTATEMENT:
            return self.postVisitDistributeByBlockStatement(node)
        elif node.type == NodeType.SortBy_BLOCKSTATEMENT:
            return self.postVisitSortByBlockStatement(node)

        # sql base expr
        elif node.type == NodeType.Literal_EXPR:
            return self.postVisitLiteral(node)
        elif node.type == NodeType.Identifier_EXPR:
            return self.postVisitIdentifier(node)
        elif node.type == NodeType.Number_EXPR:
            return self.postVisitNumber(node)
        elif node.type == NodeType.Column_EXPR:
            return self.postVisitColumn(node)
        elif node.type == NodeType.AllColumns_EXPR:
            return self.postVisitAllColumns(node)
        elif node.type == NodeType.ArrayAccess_EXPR:
            return self.postVisitArrayAccess(node)
        elif node.type == NodeType.TupleAccess_EXPR:
            return self.postVisitTupleAccess(node)
        elif node.type == NodeType.Arrays_EXPR:
            return self.postVisitArrays(node)
        elif node.type == NodeType.Tuples_EXPR:
            return self.postVisitTuples(node)
        elif node.type == NodeType.MapExpression_EXPR:
            return self.postVisitMapExpression(node)
        elif node.type == NodeType.Table_EXPR:
            return self.postVisitTable(node)
        elif node.type == NodeType.TableFunction_EXPR:
            return self.postVisitTableFunctionExpr(node)
        elif node.type == NodeType.Maps_EXPR:
            return self.postVisitMaps(node)

        # sql complex expr
        elif node.type == NodeType.NameExpression_EXPR:
            return self.postVisitNameExpression(node)
        elif node.type == NodeType.NestedExpression_EXPR:
            return self.postVisitNestedExpression(node)
        elif node.type == NodeType.Interval_EXPR:
            return self.postVisitInterval(node)
        elif node.type == NodeType.LambdaExpression_EXPR:
            return self.postVisitLambdaExpression(node)
        elif node.type == NodeType.CastExpr_EXPR:
            return self.postVisitCastExpr(node)
        elif node.type == NodeType.RatioExpr_EXPR:
            return self.postVisitRatioExpr(node)
        elif node.type == NodeType.TopExpr_EXPR:
            return self.postVisitTopExpr(node)
        elif node.type == NodeType.LimitExpr_EXPR:
            return self.postVisitLimitExpr(node)
        elif node.type == NodeType.JoinConstraintExpr_EXPR:
            return self.postVisitJoinConstraintExpr(node)
        elif node.type == NodeType.OrderExpr_EXPR:
            return self.postVisitOrderExpr(node)
        elif node.type == NodeType.EnumExpr_EXPR:
            return self.postVisitEnumExpr(node)
        elif node.type == NodeType.DateExpr_EXPR:
            return self.postVisitDateExpr(node)
        elif node.type == NodeType.TokenDefinitionExpr_EXPR:
            return self.postVisitTokenDefinitionExpr(node)
        elif node.type == NodeType.SelectItem_EXPR:
            return self.postVisitSelectItem(node)
        elif node.type == NodeType.SampleExpr_EXPR:
            return self.postVisitSampleExpr(node)
        elif node.type == NodeType.ValueTypeDefinitionExpr_EXPR:
            return self.postVisitValueTypeDefinitionExpr(node)
        elif node.type == NodeType.FormatExpr_EXPR:
            return self.postVisitFormatExpr(node)
        elif node.type == NodeType.Hive_BinaryExpr_EXPR:
            return self.postVisitBinaryExpr(node)

        # sql agg functiong
        elif node.type == NodeType.SqlAggFunction_EXPR:
            return self.postVisitSqlAggFunction(node)
        elif node.type == NodeType.SqlCountFunction_EXPR:
            return self.postVisitSqlCountFunction(node)
        elif node.type == NodeType.SqlMinFunction_EXPR:
            return self.postVisitSqlMinFunction(node)
        elif node.type == NodeType.SqlMaxFunction_EXPR:
            return self.postVisitSqlMaxFunction(node)
        elif node.type == NodeType.SqlSumFunction_EXPR:
            return self.postVisitSqlSumFunction(node)
        elif node.type == NodeType.SqlAvgFunction_EXPR:
            return self.postVisitSqlAvgFunction(node)
        elif node.type == NodeType.SqlVarPopFunction_EXPR:
            return self.postVisitSqlVarPopFunction(node)
        elif node.type == NodeType.SqlVarSampFunction_EXPR:
            return self.postVisitSqlVarSampFunction(node)
        elif node.type == NodeType.SqlStdPopFunction_EXPR:
            return self.postVisitSqlStdPopFunction(node)
        elif node.type == NodeType.SqlStdSampFunction_EXPR:
            return self.postVisitSqlStdSampFunction(node)

        # sql arithmetic
        elif node.type == NodeType.NegateExpression_EXPR:
            return self.postVisitNegateExpression(node)
        elif node.type == NodeType.MultiplyExpression_EXPR:
            return self.postVisitMultiplyExpression(node)
        elif node.type == NodeType.DivideExpression_EXPR:
            return self.postVisitDivideExpression(node)
        elif node.type == NodeType.ModuloExpression_EXPR:
            return self.postVisitModuloExpression(node)
        elif node.type == NodeType.AdditionExpression_EXPR:
            return self.postVisitAdditionExpression(node)
        elif node.type == NodeType.SubtractionExpression_EXPR:
            return self.postVisitSubtractionExpression(node)
        elif node.type == NodeType.DivExpression_EXPR:
            return self.postVisitDivExpression(node)

        # sql cond expression
        elif node.type == NodeType.IfExpression_EXPR:
            return self.postVisitIfExpression(node)
        elif node.type == NodeType.IIFFunction_EXPR:
            return self.postVisitIIFFunction(node)
        elif node.type == NodeType.MultiIfExpression_EXPR:
            return self.postVisitMultiIfExpression(node)
        elif node.type == NodeType.CaseExpression_EXPR:
            return self.postVisitCaseExpression(node)
        elif node.type == NodeType.WhenExpression_EXPR:
            return self.postVisitWhenExpression(node)
        elif node.type == NodeType.TernaryExpression_EXPR:
            return self.postVisitTernaryExpression(node)
        elif node.type == NodeType.Hive_NVLExpression_EXPR:
            return self.postVisitNvlFuncExpressio(node)
        elif node.type == NodeType.CoalesceFunction_EXPR:
            return self.postVisitCoalesceFuncExpression(node)
        elif node.type == NodeType.Hive_NullIfFunction_EXPR:
            return self.postVisitNullIfFuncExpression(node)
        elif node.type == NodeType.Hive_AssertTrueFunction_EXPR:
            return self.postVisitAssertTrueFuncExpression(node)

        # sql function
        elif node.type == NodeType.CommonFunction_EXPR:
            return self.postVisitCommonFunction(node)
        elif node.type == NodeType.ExtractFunction_EXPR:
            return self.postVisitExtractFunction(node)
        elif node.type == NodeType.MathFunction_EXPR:
            return self.postVisitMathFunction(node)
        elif node.type == NodeType.BareFunction_EXPR:
            return self.postVisitBareFunction(node)
        elif node.type == NodeType.RoundFunction_EXPR:
            return self.postVisitRoundFunction(node)
        elif node.type == NodeType.PowerFunction_EXPR:
            return self.postVisitPowerFunction(node)
        elif node.type == NodeType.QuantilesFunction_EXPR:
            return self.postVisitQuantilesFunction(node)
        elif node.type == NodeType.Quantiles2Function_EXPR:
            return self.postVisitQuantiles2Function(node)
        elif node.type == NodeType.Quantiles3Function_EXPR:
            return self.postVisitQuantiles3Function(node)
        elif node.type == NodeType.ClickHouseCommonFunction_EXPR:
            return self.postVisitClickHouseCommonFunction(node)
        elif node.type == NodeType.TrimFunction_EXPR:
            return self.postVisitTrimFunction(node)
        elif node.type == NodeType.ColumnsFunction_EXPR:
            return self.postVisitColumnsFunction(node)
        elif node.type == NodeType.ToTypeNameFunction_EXPR:
            return self.postVisitToTypeNameFunction(node)

        # sql logical bool
        elif node.type == NodeType.BinaryEqual_EXPR:
            return self.postVisitBinaryEqual(node)
        elif node.type == NodeType.LogicalEqual_EXPR:
            return self.postVisitLogicalEqual(node)
        elif node.type == NodeType.LogicalNot_EXPR:
            return self.postVisitLogicalNot(node)
        elif node.type == NodeType.LogicalAnd_EXPR:
            return self.postVisitLogicalAnd(node)
        elif node.type == NodeType.LogicalOr_EXPR:
            return self.postVisitLogicalOr(node)
        elif node.type == NodeType.LogicalConcat_EXPR:
            return self.postVisitLogicalConcat(node)
        elif node.type == NodeType.LogicalIsNull_EXPR:
            return self.postVisitLogicalIsNull(node)
        elif node.type == NodeType.LogicalCompare_EXPR:
            return self.postVisitLogicalCompare(node)
        elif node.type == NodeType.LogicalIn_EXPR:
            return self.postVisitLogicalIn(node)
        elif node.type == NodeType.LogicalLike_EXPR:
            return self.postVisitLogicalLike(node)
        elif node.type == NodeType.LogicalBetween_EXPR:
            return self.postVisitLogicalBetween(node)
        elif node.type == NodeType.LogicalIsTrue_EXPR:
            return self.postVisitLogicalIsTrue(node)
        elif node.type == NodeType.LogicalExistsQuery_EXPR:
            return self.postVisitExistsQuery(node)

        # sql table source
        elif node.type == NodeType.SqlTableSource:
            return self.postVisitSqlTableSource(node)
        elif node.type == NodeType.SqlTableJoinSource:
            return self.postVisitSqlTableJoinSource(node)
        elif node.type == NodeType.SqlUnionSource:
            return self.postVisitSqlUnionSource(node)
        elif node.type == NodeType.SqlSubquerySource:
            return self.postVisitSqlSubquerySource(node)
        elif node.type == NodeType.SqlArrayJoinSource:
            return self.postVisitSqlArrayJoinSource(node)
        elif node.type == NodeType.SqlFusionMergeSource:
            return self.postVisitFusionMergeSource(node)



