# Generated from Hive.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .hive_parser import HiveParser
else:
    from HiveParser import HiveParser


# This class defines a complete listener for a parse tree produced by HiveParser.
class HiveListener(ParseTreeListener):

    # Enter a parse tree produced by HiveParser#query.
    def enterQuery(self, ctx: HiveParser.QueryContext):
        pass

    # Exit a parse tree produced by HiveParser#query.
    def exitQuery(self, ctx: HiveParser.QueryContext):
        pass

    # Enter a parse tree produced by HiveParser#selectUnionStmt.
    def enterSelectUnionStmt(self, ctx: HiveParser.SelectUnionStmtContext):
        pass

    # Exit a parse tree produced by HiveParser#selectUnionStmt.
    def exitSelectUnionStmt(self, ctx: HiveParser.SelectUnionStmtContext):
        pass

    # Enter a parse tree produced by HiveParser#StmtUnionAll.
    def enterStmtUnionAll(self, ctx: HiveParser.StmtUnionAllContext):
        pass

    # Exit a parse tree produced by HiveParser#StmtUnionAll.
    def exitStmtUnionAll(self, ctx: HiveParser.StmtUnionAllContext):
        pass

    # Enter a parse tree produced by HiveParser#StmtUnionDistinct.
    def enterStmtUnionDistinct(self, ctx: HiveParser.StmtUnionDistinctContext):
        pass

    # Exit a parse tree produced by HiveParser#StmtUnionDistinct.
    def exitStmtUnionDistinct(self, ctx: HiveParser.StmtUnionDistinctContext):
        pass

    # Enter a parse tree produced by HiveParser#StmtUnion.
    def enterStmtUnion(self, ctx: HiveParser.StmtUnionContext):
        pass

    # Exit a parse tree produced by HiveParser#StmtUnion.
    def exitStmtUnion(self, ctx: HiveParser.StmtUnionContext):
        pass

    # Enter a parse tree produced by HiveParser#selectStmtWithParens.
    def enterSelectStmtWithParens(self, ctx: HiveParser.SelectStmtWithParensContext):
        pass

    # Exit a parse tree produced by HiveParser#selectStmtWithParens.
    def exitSelectStmtWithParens(self, ctx: HiveParser.SelectStmtWithParensContext):
        pass

    # Enter a parse tree produced by HiveParser#selectStmt.
    def enterSelectStmt(self, ctx: HiveParser.SelectStmtContext):
        pass

    # Exit a parse tree produced by HiveParser#selectStmt.
    def exitSelectStmt(self, ctx: HiveParser.SelectStmtContext):
        pass

    # Enter a parse tree produced by HiveParser#selectClause.
    def enterSelectClause(self, ctx: HiveParser.SelectClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#selectClause.
    def exitSelectClause(self, ctx: HiveParser.SelectClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#withClause.
    def enterWithClause(self, ctx: HiveParser.WithClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#withClause.
    def exitWithClause(self, ctx: HiveParser.WithClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#topClause.
    def enterTopClause(self, ctx: HiveParser.TopClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#topClause.
    def exitTopClause(self, ctx: HiveParser.TopClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#fromClause.
    def enterFromClause(self, ctx: HiveParser.FromClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#fromClause.
    def exitFromClause(self, ctx: HiveParser.FromClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#WhereExpr.
    def enterWhereExpr(self, ctx: HiveParser.WhereExprContext):
        pass

    # Exit a parse tree produced by HiveParser#WhereExpr.
    def exitWhereExpr(self, ctx: HiveParser.WhereExprContext):
        pass

    # Enter a parse tree produced by HiveParser#WhereExistsQuery.
    def enterWhereExistsQuery(self, ctx: HiveParser.WhereExistsQueryContext):
        pass

    # Exit a parse tree produced by HiveParser#WhereExistsQuery.
    def exitWhereExistsQuery(self, ctx: HiveParser.WhereExistsQueryContext):
        pass

    # Enter a parse tree produced by HiveParser#GroupFrontCr.
    def enterGroupFrontCr(self, ctx: HiveParser.GroupFrontCrContext):
        pass

    # Exit a parse tree produced by HiveParser#GroupFrontCr.
    def exitGroupFrontCr(self, ctx: HiveParser.GroupFrontCrContext):
        pass

    # Enter a parse tree produced by HiveParser#GroupNoFrontCr.
    def enterGroupNoFrontCr(self, ctx: HiveParser.GroupNoFrontCrContext):
        pass

    # Exit a parse tree produced by HiveParser#GroupNoFrontCr.
    def exitGroupNoFrontCr(self, ctx: HiveParser.GroupNoFrontCrContext):
        pass

    # Enter a parse tree produced by HiveParser#havingClause.
    def enterHavingClause(self, ctx: HiveParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#havingClause.
    def exitHavingClause(self, ctx: HiveParser.HavingClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#orderByClause.
    def enterOrderByClause(self, ctx: HiveParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#orderByClause.
    def exitOrderByClause(self, ctx: HiveParser.OrderByClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#clusterByClause.
    def enterClusterByClause(self, ctx: HiveParser.ClusterByClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#clusterByClause.
    def exitClusterByClause(self, ctx: HiveParser.ClusterByClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#distributeByClause.
    def enterDistributeByClause(self, ctx: HiveParser.DistributeByClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#distributeByClause.
    def exitDistributeByClause(self, ctx: HiveParser.DistributeByClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#sortByClause.
    def enterSortByClause(self, ctx: HiveParser.SortByClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#sortByClause.
    def exitSortByClause(self, ctx: HiveParser.SortByClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#limitClause.
    def enterLimitClause(self, ctx: HiveParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#limitClause.
    def exitLimitClause(self, ctx: HiveParser.LimitClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#GroupWithCube.
    def enterGroupWithCube(self, ctx: HiveParser.GroupWithCubeContext):
        pass

    # Exit a parse tree produced by HiveParser#GroupWithCube.
    def exitGroupWithCube(self, ctx: HiveParser.GroupWithCubeContext):
        pass

    # Enter a parse tree produced by HiveParser#GroupWithRollup.
    def enterGroupWithRollup(self, ctx: HiveParser.GroupWithRollupContext):
        pass

    # Exit a parse tree produced by HiveParser#GroupWithRollup.
    def exitGroupWithRollup(self, ctx: HiveParser.GroupWithRollupContext):
        pass

    # Enter a parse tree produced by HiveParser#GroupWithTotals.
    def enterGroupWithTotals(self, ctx: HiveParser.GroupWithTotalsContext):
        pass

    # Exit a parse tree produced by HiveParser#GroupWithTotals.
    def exitGroupWithTotals(self, ctx: HiveParser.GroupWithTotalsContext):
        pass

    # Enter a parse tree produced by HiveParser#JoinExprOp.
    def enterJoinExprOp(self, ctx: HiveParser.JoinExprOpContext):
        pass

    # Exit a parse tree produced by HiveParser#JoinExprOp.
    def exitJoinExprOp(self, ctx: HiveParser.JoinExprOpContext):
        pass

    # Enter a parse tree produced by HiveParser#JoinExprTable.
    def enterJoinExprTable(self, ctx: HiveParser.JoinExprTableContext):
        pass

    # Exit a parse tree produced by HiveParser#JoinExprTable.
    def exitJoinExprTable(self, ctx: HiveParser.JoinExprTableContext):
        pass

    # Enter a parse tree produced by HiveParser#JoinExprParens.
    def enterJoinExprParens(self, ctx: HiveParser.JoinExprParensContext):
        pass

    # Exit a parse tree produced by HiveParser#JoinExprParens.
    def exitJoinExprParens(self, ctx: HiveParser.JoinExprParensContext):
        pass

    # Enter a parse tree produced by HiveParser#JoinExprCrossOp.
    def enterJoinExprCrossOp(self, ctx: HiveParser.JoinExprCrossOpContext):
        pass

    # Exit a parse tree produced by HiveParser#JoinExprCrossOp.
    def exitJoinExprCrossOp(self, ctx: HiveParser.JoinExprCrossOpContext):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpInner1.
    def enterJoinOpInner1(self, ctx: HiveParser.JoinOpInner1Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpInner1.
    def exitJoinOpInner1(self, ctx: HiveParser.JoinOpInner1Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpInner2.
    def enterJoinOpInner2(self, ctx: HiveParser.JoinOpInner2Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpInner2.
    def exitJoinOpInner2(self, ctx: HiveParser.JoinOpInner2Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpInner3.
    def enterJoinOpInner3(self, ctx: HiveParser.JoinOpInner3Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpInner3.
    def exitJoinOpInner3(self, ctx: HiveParser.JoinOpInner3Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpLeftRight1.
    def enterJoinOpLeftRight1(self, ctx: HiveParser.JoinOpLeftRight1Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpLeftRight1.
    def exitJoinOpLeftRight1(self, ctx: HiveParser.JoinOpLeftRight1Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpLeftRight2.
    def enterJoinOpLeftRight2(self, ctx: HiveParser.JoinOpLeftRight2Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpLeftRight2.
    def exitJoinOpLeftRight2(self, ctx: HiveParser.JoinOpLeftRight2Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpFull1.
    def enterJoinOpFull1(self, ctx: HiveParser.JoinOpFull1Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpFull1.
    def exitJoinOpFull1(self, ctx: HiveParser.JoinOpFull1Context):
        pass

    # Enter a parse tree produced by HiveParser#JoinOpFull2.
    def enterJoinOpFull2(self, ctx: HiveParser.JoinOpFull2Context):
        pass

    # Exit a parse tree produced by HiveParser#JoinOpFull2.
    def exitJoinOpFull2(self, ctx: HiveParser.JoinOpFull2Context):
        pass

    # Enter a parse tree produced by HiveParser#joinOpCross.
    def enterJoinOpCross(self, ctx: HiveParser.JoinOpCrossContext):
        pass

    # Exit a parse tree produced by HiveParser#joinOpCross.
    def exitJoinOpCross(self, ctx: HiveParser.JoinOpCrossContext):
        pass

    # Enter a parse tree produced by HiveParser#joinConstraintClause.
    def enterJoinConstraintClause(self, ctx: HiveParser.JoinConstraintClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#joinConstraintClause.
    def exitJoinConstraintClause(self, ctx: HiveParser.JoinConstraintClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#sampleClause.
    def enterSampleClause(self, ctx: HiveParser.SampleClauseContext):
        pass

    # Exit a parse tree produced by HiveParser#sampleClause.
    def exitSampleClause(self, ctx: HiveParser.SampleClauseContext):
        pass

    # Enter a parse tree produced by HiveParser#limitExpr.
    def enterLimitExpr(self, ctx: HiveParser.LimitExprContext):
        pass

    # Exit a parse tree produced by HiveParser#limitExpr.
    def exitLimitExpr(self, ctx: HiveParser.LimitExprContext):
        pass

    # Enter a parse tree produced by HiveParser#orderExprList.
    def enterOrderExprList(self, ctx: HiveParser.OrderExprListContext):
        pass

    # Exit a parse tree produced by HiveParser#orderExprList.
    def exitOrderExprList(self, ctx: HiveParser.OrderExprListContext):
        pass

    # Enter a parse tree produced by HiveParser#orderExpr.
    def enterOrderExpr(self, ctx: HiveParser.OrderExprContext):
        pass

    # Exit a parse tree produced by HiveParser#orderExpr.
    def exitOrderExpr(self, ctx: HiveParser.OrderExprContext):
        pass

    # Enter a parse tree produced by HiveParser#ratioExpr.
    def enterRatioExpr(self, ctx: HiveParser.RatioExprContext):
        pass

    # Exit a parse tree produced by HiveParser#ratioExpr.
    def exitRatioExpr(self, ctx: HiveParser.RatioExprContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeExprSimple.
    def enterColumnTypeExprSimple(self, ctx: HiveParser.ColumnTypeExprSimpleContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeExprSimple.
    def exitColumnTypeExprSimple(self, ctx: HiveParser.ColumnTypeExprSimpleContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeExprNested.
    def enterColumnTypeExprNested(self, ctx: HiveParser.ColumnTypeExprNestedContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeExprNested.
    def exitColumnTypeExprNested(self, ctx: HiveParser.ColumnTypeExprNestedContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeExprEnum.
    def enterColumnTypeExprEnum(self, ctx: HiveParser.ColumnTypeExprEnumContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeExprEnum.
    def exitColumnTypeExprEnum(self, ctx: HiveParser.ColumnTypeExprEnumContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeExprComplex.
    def enterColumnTypeExprComplex(self, ctx: HiveParser.ColumnTypeExprComplexContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeExprComplex.
    def exitColumnTypeExprComplex(self, ctx: HiveParser.ColumnTypeExprComplexContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeDecimal.
    def enterColumnTypeDecimal(self, ctx: HiveParser.ColumnTypeDecimalContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeDecimal.
    def exitColumnTypeDecimal(self, ctx: HiveParser.ColumnTypeDecimalContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeExprParam.
    def enterColumnTypeExprParam(self, ctx: HiveParser.ColumnTypeExprParamContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeExprParam.
    def exitColumnTypeExprParam(self, ctx: HiveParser.ColumnTypeExprParamContext):
        pass

    # Enter a parse tree produced by HiveParser#columnDefinitionExpr.
    def enterColumnDefinitionExpr(self, ctx: HiveParser.ColumnDefinitionExprContext):
        pass

    # Exit a parse tree produced by HiveParser#columnDefinitionExpr.
    def exitColumnDefinitionExpr(self, ctx: HiveParser.ColumnDefinitionExprContext):
        pass

    # Enter a parse tree produced by HiveParser#columnExprList.
    def enterColumnExprList(self, ctx: HiveParser.ColumnExprListContext):
        pass

    # Exit a parse tree produced by HiveParser#columnExprList.
    def exitColumnExprList(self, ctx: HiveParser.ColumnExprListContext):
        pass

    # Enter a parse tree produced by HiveParser#columnExprWhen.
    def enterColumnExprWhen(self, ctx: HiveParser.ColumnExprWhenContext):
        pass

    # Exit a parse tree produced by HiveParser#columnExprWhen.
    def exitColumnExprWhen(self, ctx: HiveParser.ColumnExprWhenContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnsExprAsterisk.
    def enterColumnsExprAsterisk(self, ctx: HiveParser.ColumnsExprAsteriskContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnsExprAsterisk.
    def exitColumnsExprAsterisk(self, ctx: HiveParser.ColumnsExprAsteriskContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnsExprSubquery.
    def enterColumnsExprSubquery(self, ctx: HiveParser.ColumnsExprSubqueryContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnsExprSubquery.
    def exitColumnsExprSubquery(self, ctx: HiveParser.ColumnsExprSubqueryContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnsExprColumn.
    def enterColumnsExprColumn(self, ctx: HiveParser.ColumnsExprColumnContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnsExprColumn.
    def exitColumnsExprColumn(self, ctx: HiveParser.ColumnsExprColumnContext):
        pass

    # Enter a parse tree produced by HiveParser#caseExpr.
    def enterCaseExpr(self, ctx: HiveParser.CaseExprContext):
        pass

    # Exit a parse tree produced by HiveParser#caseExpr.
    def exitCaseExpr(self, ctx: HiveParser.CaseExprContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprTernaryOp.
    def enterColumnExprTernaryOp(self, ctx: HiveParser.ColumnExprTernaryOpContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprTernaryOp.
    def exitColumnExprTernaryOp(self, ctx: HiveParser.ColumnExprTernaryOpContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprAlias.
    def enterColumnExprAlias(self, ctx: HiveParser.ColumnExprAliasContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprAlias.
    def exitColumnExprAlias(self, ctx: HiveParser.ColumnExprAliasContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprExtract.
    def enterColumnExprExtract(self, ctx: HiveParser.ColumnExprExtractContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprExtract.
    def exitColumnExprExtract(self, ctx: HiveParser.ColumnExprExtractContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprNegate.
    def enterColumnExprNegate(self, ctx: HiveParser.ColumnExprNegateContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprNegate.
    def exitColumnExprNegate(self, ctx: HiveParser.ColumnExprNegateContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprSubquery.
    def enterColumnExprSubquery(self, ctx: HiveParser.ColumnExprSubqueryContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprSubquery.
    def exitColumnExprSubquery(self, ctx: HiveParser.ColumnExprSubqueryContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprLiteral.
    def enterColumnExprLiteral(self, ctx: HiveParser.ColumnExprLiteralContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprLiteral.
    def exitColumnExprLiteral(self, ctx: HiveParser.ColumnExprLiteralContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprArray.
    def enterColumnExprArray(self, ctx: HiveParser.ColumnExprArrayContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprArray.
    def exitColumnExprArray(self, ctx: HiveParser.ColumnExprArrayContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprSubstring.
    def enterColumnExprSubstring(self, ctx: HiveParser.ColumnExprSubstringContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprSubstring.
    def exitColumnExprSubstring(self, ctx: HiveParser.ColumnExprSubstringContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprCast.
    def enterColumnExprCast(self, ctx: HiveParser.ColumnExprCastContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprCast.
    def exitColumnExprCast(self, ctx: HiveParser.ColumnExprCastContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprMultiIfExpr.
    def enterColumnExprMultiIfExpr(self, ctx: HiveParser.ColumnExprMultiIfExprContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprMultiIfExpr.
    def exitColumnExprMultiIfExpr(self, ctx: HiveParser.ColumnExprMultiIfExprContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprOr.
    def enterColumnExprOr(self, ctx: HiveParser.ColumnExprOrContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprOr.
    def exitColumnExprOr(self, ctx: HiveParser.ColumnExprOrContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnTypeDefinition.
    def enterColumnTypeDefinition(self, ctx: HiveParser.ColumnTypeDefinitionContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnTypeDefinition.
    def exitColumnTypeDefinition(self, ctx: HiveParser.ColumnTypeDefinitionContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprPowFunction.
    def enterColumnExprPowFunction(self, ctx: HiveParser.ColumnExprPowFunctionContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprPowFunction.
    def exitColumnExprPowFunction(self, ctx: HiveParser.ColumnExprPowFunctionContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprPrecedence1.
    def enterColumnExprPrecedence1(self, ctx: HiveParser.ColumnExprPrecedence1Context):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprPrecedence1.
    def exitColumnExprPrecedence1(self, ctx: HiveParser.ColumnExprPrecedence1Context):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprBinaryCast.
    def enterColumnExprBinaryCast(self, ctx: HiveParser.ColumnExprBinaryCastContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprBinaryCast.
    def exitColumnExprBinaryCast(self, ctx: HiveParser.ColumnExprBinaryCastContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprPrecedence2.
    def enterColumnExprPrecedence2(self, ctx: HiveParser.ColumnExprPrecedence2Context):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprPrecedence2.
    def exitColumnExprPrecedence2(self, ctx: HiveParser.ColumnExprPrecedence2Context):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprPrecedence3.
    def enterColumnExprPrecedence3(self, ctx: HiveParser.ColumnExprPrecedence3Context):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprPrecedence3.
    def exitColumnExprPrecedence3(self, ctx: HiveParser.ColumnExprPrecedence3Context):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprInterval.
    def enterColumnExprInterval(self, ctx: HiveParser.ColumnExprIntervalContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprInterval.
    def exitColumnExprInterval(self, ctx: HiveParser.ColumnExprIntervalContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprIsNull.
    def enterColumnExprIsNull(self, ctx: HiveParser.ColumnExprIsNullContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprIsNull.
    def exitColumnExprIsNull(self, ctx: HiveParser.ColumnExprIsNullContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprIsTrue.
    def enterColumnExprIsTrue(self, ctx: HiveParser.ColumnExprIsTrueContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprIsTrue.
    def exitColumnExprIsTrue(self, ctx: HiveParser.ColumnExprIsTrueContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprTrim.
    def enterColumnExprTrim(self, ctx: HiveParser.ColumnExprTrimContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprTrim.
    def exitColumnExprTrim(self, ctx: HiveParser.ColumnExprTrimContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprTuple.
    def enterColumnExprTuple(self, ctx: HiveParser.ColumnExprTupleContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprTuple.
    def exitColumnExprTuple(self, ctx: HiveParser.ColumnExprTupleContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprArrayAccess.
    def enterColumnExprArrayAccess(self, ctx: HiveParser.ColumnExprArrayAccessContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprArrayAccess.
    def exitColumnExprArrayAccess(self, ctx: HiveParser.ColumnExprArrayAccessContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprBetween.
    def enterColumnExprBetween(self, ctx: HiveParser.ColumnExprBetweenContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprBetween.
    def exitColumnExprBetween(self, ctx: HiveParser.ColumnExprBetweenContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprParens.
    def enterColumnExprParens(self, ctx: HiveParser.ColumnExprParensContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprParens.
    def exitColumnExprParens(self, ctx: HiveParser.ColumnExprParensContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprTimestamp.
    def enterColumnExprTimestamp(self, ctx: HiveParser.ColumnExprTimestampContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprTimestamp.
    def exitColumnExprTimestamp(self, ctx: HiveParser.ColumnExprTimestampContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprAggFunction.
    def enterColumnExprAggFunction(self, ctx: HiveParser.ColumnExprAggFunctionContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprAggFunction.
    def exitColumnExprAggFunction(self, ctx: HiveParser.ColumnExprAggFunctionContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprIfExpr.
    def enterColumnExprIfExpr(self, ctx: HiveParser.ColumnExprIfExprContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprIfExpr.
    def exitColumnExprIfExpr(self, ctx: HiveParser.ColumnExprIfExprContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprAliasSubquery.
    def enterColumnExprAliasSubquery(self, ctx: HiveParser.ColumnExprAliasSubqueryContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprAliasSubquery.
    def exitColumnExprAliasSubquery(self, ctx: HiveParser.ColumnExprAliasSubqueryContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprAnd.
    def enterColumnExprAnd(self, ctx: HiveParser.ColumnExprAndContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprAnd.
    def exitColumnExprAnd(self, ctx: HiveParser.ColumnExprAndContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprTupleAccess.
    def enterColumnExprTupleAccess(self, ctx: HiveParser.ColumnExprTupleAccessContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprTupleAccess.
    def exitColumnExprTupleAccess(self, ctx: HiveParser.ColumnExprTupleAccessContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprCase.
    def enterColumnExprCase(self, ctx: HiveParser.ColumnExprCaseContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprCase.
    def exitColumnExprCase(self, ctx: HiveParser.ColumnExprCaseContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprSumCaseFunction.
    def enterColumnExprSumCaseFunction(self, ctx: HiveParser.ColumnExprSumCaseFunctionContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprSumCaseFunction.
    def exitColumnExprSumCaseFunction(self, ctx: HiveParser.ColumnExprSumCaseFunctionContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprDate.
    def enterColumnExprDate(self, ctx: HiveParser.ColumnExprDateContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprDate.
    def exitColumnExprDate(self, ctx: HiveParser.ColumnExprDateContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprNot.
    def enterColumnExprNot(self, ctx: HiveParser.ColumnExprNotContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprNot.
    def exitColumnExprNot(self, ctx: HiveParser.ColumnExprNotContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprIdentifier.
    def enterColumnExprIdentifier(self, ctx: HiveParser.ColumnExprIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprIdentifier.
    def exitColumnExprIdentifier(self, ctx: HiveParser.ColumnExprIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprFunction.
    def enterColumnExprFunction(self, ctx: HiveParser.ColumnExprFunctionContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprFunction.
    def exitColumnExprFunction(self, ctx: HiveParser.ColumnExprFunctionContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnExprAsterisk.
    def enterColumnExprAsterisk(self, ctx: HiveParser.ColumnExprAsteriskContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnExprAsterisk.
    def exitColumnExprAsterisk(self, ctx: HiveParser.ColumnExprAsteriskContext):
        pass

    # Enter a parse tree produced by HiveParser#ColumnQuoteExpr.
    def enterColumnQuoteExpr(self, ctx: HiveParser.ColumnQuoteExprContext):
        pass

    # Exit a parse tree produced by HiveParser#ColumnQuoteExpr.
    def exitColumnQuoteExpr(self, ctx: HiveParser.ColumnQuoteExprContext):
        pass

    # Enter a parse tree produced by HiveParser#columnArgList.
    def enterColumnArgList(self, ctx: HiveParser.ColumnArgListContext):
        pass

    # Exit a parse tree produced by HiveParser#columnArgList.
    def exitColumnArgList(self, ctx: HiveParser.ColumnArgListContext):
        pass

    # Enter a parse tree produced by HiveParser#columnArgExpr.
    def enterColumnArgExpr(self, ctx: HiveParser.ColumnArgExprContext):
        pass

    # Exit a parse tree produced by HiveParser#columnArgExpr.
    def exitColumnArgExpr(self, ctx: HiveParser.ColumnArgExprContext):
        pass

    # Enter a parse tree produced by HiveParser#columnLambdaExpr.
    def enterColumnLambdaExpr(self, ctx: HiveParser.ColumnLambdaExprContext):
        pass

    # Exit a parse tree produced by HiveParser#columnLambdaExpr.
    def exitColumnLambdaExpr(self, ctx: HiveParser.ColumnLambdaExprContext):
        pass

    # Enter a parse tree produced by HiveParser#columnIdentifier.
    def enterColumnIdentifier(self, ctx: HiveParser.ColumnIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#columnIdentifier.
    def exitColumnIdentifier(self, ctx: HiveParser.ColumnIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#nestedIdentifier.
    def enterNestedIdentifier(self, ctx: HiveParser.NestedIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#nestedIdentifier.
    def exitNestedIdentifier(self, ctx: HiveParser.NestedIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#TableExprIdentifier.
    def enterTableExprIdentifier(self, ctx: HiveParser.TableExprIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#TableExprIdentifier.
    def exitTableExprIdentifier(self, ctx: HiveParser.TableExprIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#TableExprSubquery.
    def enterTableExprSubquery(self, ctx: HiveParser.TableExprSubqueryContext):
        pass

    # Exit a parse tree produced by HiveParser#TableExprSubquery.
    def exitTableExprSubquery(self, ctx: HiveParser.TableExprSubqueryContext):
        pass

    # Enter a parse tree produced by HiveParser#TableExprAlias.
    def enterTableExprAlias(self, ctx: HiveParser.TableExprAliasContext):
        pass

    # Exit a parse tree produced by HiveParser#TableExprAlias.
    def exitTableExprAlias(self, ctx: HiveParser.TableExprAliasContext):
        pass

    # Enter a parse tree produced by HiveParser#TableExprFunction.
    def enterTableExprFunction(self, ctx: HiveParser.TableExprFunctionContext):
        pass

    # Exit a parse tree produced by HiveParser#TableExprFunction.
    def exitTableExprFunction(self, ctx: HiveParser.TableExprFunctionContext):
        pass

    # Enter a parse tree produced by HiveParser#tableFunctionExpr.
    def enterTableFunctionExpr(self, ctx: HiveParser.TableFunctionExprContext):
        pass

    # Exit a parse tree produced by HiveParser#tableFunctionExpr.
    def exitTableFunctionExpr(self, ctx: HiveParser.TableFunctionExprContext):
        pass

    # Enter a parse tree produced by HiveParser#tableIdentifier.
    def enterTableIdentifier(self, ctx: HiveParser.TableIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#tableIdentifier.
    def exitTableIdentifier(self, ctx: HiveParser.TableIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#tableArgList.
    def enterTableArgList(self, ctx: HiveParser.TableArgListContext):
        pass

    # Exit a parse tree produced by HiveParser#tableArgList.
    def exitTableArgList(self, ctx: HiveParser.TableArgListContext):
        pass

    # Enter a parse tree produced by HiveParser#tableArgExpr.
    def enterTableArgExpr(self, ctx: HiveParser.TableArgExprContext):
        pass

    # Exit a parse tree produced by HiveParser#tableArgExpr.
    def exitTableArgExpr(self, ctx: HiveParser.TableArgExprContext):
        pass

    # Enter a parse tree produced by HiveParser#databaseIdentifier.
    def enterDatabaseIdentifier(self, ctx: HiveParser.DatabaseIdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#databaseIdentifier.
    def exitDatabaseIdentifier(self, ctx: HiveParser.DatabaseIdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#floatingLiteral.
    def enterFloatingLiteral(self, ctx: HiveParser.FloatingLiteralContext):
        pass

    # Exit a parse tree produced by HiveParser#floatingLiteral.
    def exitFloatingLiteral(self, ctx: HiveParser.FloatingLiteralContext):
        pass

    # Enter a parse tree produced by HiveParser#numberLiteral.
    def enterNumberLiteral(self, ctx: HiveParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by HiveParser#numberLiteral.
    def exitNumberLiteral(self, ctx: HiveParser.NumberLiteralContext):
        pass

    # Enter a parse tree produced by HiveParser#numliteral.
    def enterNumliteral(self, ctx: HiveParser.NumliteralContext):
        pass

    # Exit a parse tree produced by HiveParser#numliteral.
    def exitNumliteral(self, ctx: HiveParser.NumliteralContext):
        pass

    # Enter a parse tree produced by HiveParser#stringliteral.
    def enterStringliteral(self, ctx: HiveParser.StringliteralContext):
        pass

    # Exit a parse tree produced by HiveParser#stringliteral.
    def exitStringliteral(self, ctx: HiveParser.StringliteralContext):
        pass

    # Enter a parse tree produced by HiveParser#nullliteral.
    def enterNullliteral(self, ctx: HiveParser.NullliteralContext):
        pass

    # Exit a parse tree produced by HiveParser#nullliteral.
    def exitNullliteral(self, ctx: HiveParser.NullliteralContext):
        pass

    # Enter a parse tree produced by HiveParser#interval.
    def enterInterval(self, ctx: HiveParser.IntervalContext):
        pass

    # Exit a parse tree produced by HiveParser#interval.
    def exitInterval(self, ctx: HiveParser.IntervalContext):
        pass

    # Enter a parse tree produced by HiveParser#aggregateFunctionName.
    def enterAggregateFunctionName(self, ctx: HiveParser.AggregateFunctionNameContext):
        pass

    # Exit a parse tree produced by HiveParser#aggregateFunctionName.
    def exitAggregateFunctionName(self, ctx: HiveParser.AggregateFunctionNameContext):
        pass

    # Enter a parse tree produced by HiveParser#decimalTypeName.
    def enterDecimalTypeName(self, ctx: HiveParser.DecimalTypeNameContext):
        pass

    # Exit a parse tree produced by HiveParser#decimalTypeName.
    def exitDecimalTypeName(self, ctx: HiveParser.DecimalTypeNameContext):
        pass

    # Enter a parse tree produced by HiveParser#tupleOrArrayName.
    def enterTupleOrArrayName(self, ctx: HiveParser.TupleOrArrayNameContext):
        pass

    # Exit a parse tree produced by HiveParser#tupleOrArrayName.
    def exitTupleOrArrayName(self, ctx: HiveParser.TupleOrArrayNameContext):
        pass

    # Enter a parse tree produced by HiveParser#keyword.
    def enterKeyword(self, ctx: HiveParser.KeywordContext):
        pass

    # Exit a parse tree produced by HiveParser#keyword.
    def exitKeyword(self, ctx: HiveParser.KeywordContext):
        pass

    # Enter a parse tree produced by HiveParser#keywordForAlias.
    def enterKeywordForAlias(self, ctx: HiveParser.KeywordForAliasContext):
        pass

    # Exit a parse tree produced by HiveParser#keywordForAlias.
    def exitKeywordForAlias(self, ctx: HiveParser.KeywordForAliasContext):
        pass

    # Enter a parse tree produced by HiveParser#alias.
    def enterAlias(self, ctx: HiveParser.AliasContext):
        pass

    # Exit a parse tree produced by HiveParser#alias.
    def exitAlias(self, ctx: HiveParser.AliasContext):
        pass

    # Enter a parse tree produced by HiveParser#identifier.
    def enterIdentifier(self, ctx: HiveParser.IdentifierContext):
        pass

    # Exit a parse tree produced by HiveParser#identifier.
    def exitIdentifier(self, ctx: HiveParser.IdentifierContext):
        pass

    # Enter a parse tree produced by HiveParser#identifierOrNull.
    def enterIdentifierOrNull(self, ctx: HiveParser.IdentifierOrNullContext):
        pass

    # Exit a parse tree produced by HiveParser#identifierOrNull.
    def exitIdentifierOrNull(self, ctx: HiveParser.IdentifierOrNullContext):
        pass

    # Enter a parse tree produced by HiveParser#enumValue.
    def enterEnumValue(self, ctx: HiveParser.EnumValueContext):
        pass

    # Exit a parse tree produced by HiveParser#enumValue.
    def exitEnumValue(self, ctx: HiveParser.EnumValueContext):
        pass


del HiveParser
