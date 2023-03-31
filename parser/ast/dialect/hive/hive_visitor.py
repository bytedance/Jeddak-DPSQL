# Generated from Hive.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .hive_parser import HiveParser
else:
    from hive_parser import HiveParser


# This class defines a complete generic visitor for a parse tree produced by HiveParser.

class HiveVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HiveParser#query.
    def visitQuery(self, ctx: HiveParser.QueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#selectUnionStmt.
    def visitSelectUnionStmt(self, ctx: HiveParser.SelectUnionStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#StmtUnionAll.
    def visitStmtUnionAll(self, ctx: HiveParser.StmtUnionAllContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#StmtUnionDistinct.
    def visitStmtUnionDistinct(self, ctx: HiveParser.StmtUnionDistinctContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#StmtUnion.
    def visitStmtUnion(self, ctx: HiveParser.StmtUnionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#selectStmtWithParens.
    def visitSelectStmtWithParens(self, ctx: HiveParser.SelectStmtWithParensContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#selectStmt.
    def visitSelectStmt(self, ctx: HiveParser.SelectStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#selectClause.
    def visitSelectClause(self, ctx: HiveParser.SelectClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#withClause.
    def visitWithClause(self, ctx: HiveParser.WithClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#topClause.
    def visitTopClause(self, ctx: HiveParser.TopClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#fromClause.
    def visitFromClause(self, ctx: HiveParser.FromClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#WhereExpr.
    def visitWhereExpr(self, ctx: HiveParser.WhereExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#WhereExistsQuery.
    def visitWhereExistsQuery(self, ctx: HiveParser.WhereExistsQueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#GroupFrontCr.
    def visitGroupFrontCr(self, ctx: HiveParser.GroupFrontCrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#GroupNoFrontCr.
    def visitGroupNoFrontCr(self, ctx: HiveParser.GroupNoFrontCrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#havingClause.
    def visitHavingClause(self, ctx: HiveParser.HavingClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#orderByClause.
    def visitOrderByClause(self, ctx: HiveParser.OrderByClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#clusterByClause.
    def visitClusterByClause(self, ctx: HiveParser.ClusterByClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#distributeByClause.
    def visitDistributeByClause(self, ctx: HiveParser.DistributeByClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#sortByClause.
    def visitSortByClause(self, ctx: HiveParser.SortByClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#limitClause.
    def visitLimitClause(self, ctx: HiveParser.LimitClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#GroupWithCube.
    def visitGroupWithCube(self, ctx: HiveParser.GroupWithCubeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#GroupWithRollup.
    def visitGroupWithRollup(self, ctx: HiveParser.GroupWithRollupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#GroupWithTotals.
    def visitGroupWithTotals(self, ctx: HiveParser.GroupWithTotalsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinExprOp.
    def visitJoinExprOp(self, ctx: HiveParser.JoinExprOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinExprTable.
    def visitJoinExprTable(self, ctx: HiveParser.JoinExprTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinExprParens.
    def visitJoinExprParens(self, ctx: HiveParser.JoinExprParensContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinExprCrossOp.
    def visitJoinExprCrossOp(self, ctx: HiveParser.JoinExprCrossOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpInner1.
    def visitJoinOpInner1(self, ctx: HiveParser.JoinOpInner1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpInner2.
    def visitJoinOpInner2(self, ctx: HiveParser.JoinOpInner2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpInner3.
    def visitJoinOpInner3(self, ctx: HiveParser.JoinOpInner3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpLeftRight1.
    def visitJoinOpLeftRight1(self, ctx: HiveParser.JoinOpLeftRight1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpLeftRight2.
    def visitJoinOpLeftRight2(self, ctx: HiveParser.JoinOpLeftRight2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpFull1.
    def visitJoinOpFull1(self, ctx: HiveParser.JoinOpFull1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#JoinOpFull2.
    def visitJoinOpFull2(self, ctx: HiveParser.JoinOpFull2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#joinOpCross.
    def visitJoinOpCross(self, ctx: HiveParser.JoinOpCrossContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#joinConstraintClause.
    def visitJoinConstraintClause(self, ctx: HiveParser.JoinConstraintClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#sampleClause.
    def visitSampleClause(self, ctx: HiveParser.SampleClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#limitExpr.
    def visitLimitExpr(self, ctx: HiveParser.LimitExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#orderExprList.
    def visitOrderExprList(self, ctx: HiveParser.OrderExprListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#orderExpr.
    def visitOrderExpr(self, ctx: HiveParser.OrderExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ratioExpr.
    def visitRatioExpr(self, ctx: HiveParser.RatioExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeExprSimple.
    def visitColumnTypeExprSimple(self, ctx: HiveParser.ColumnTypeExprSimpleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeExprNested.
    def visitColumnTypeExprNested(self, ctx: HiveParser.ColumnTypeExprNestedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeExprEnum.
    def visitColumnTypeExprEnum(self, ctx: HiveParser.ColumnTypeExprEnumContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeExprComplex.
    def visitColumnTypeExprComplex(self, ctx: HiveParser.ColumnTypeExprComplexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeDecimal.
    def visitColumnTypeDecimal(self, ctx: HiveParser.ColumnTypeDecimalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeExprParam.
    def visitColumnTypeExprParam(self, ctx: HiveParser.ColumnTypeExprParamContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnDefinitionExpr.
    def visitColumnDefinitionExpr(self, ctx: HiveParser.ColumnDefinitionExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnExprList.
    def visitColumnExprList(self, ctx: HiveParser.ColumnExprListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnExprWhen.
    def visitColumnExprWhen(self, ctx: HiveParser.ColumnExprWhenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnsExprAsterisk.
    def visitColumnsExprAsterisk(self, ctx: HiveParser.ColumnsExprAsteriskContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnsExprSubquery.
    def visitColumnsExprSubquery(self, ctx: HiveParser.ColumnsExprSubqueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnsExprColumn.
    def visitColumnsExprColumn(self, ctx: HiveParser.ColumnsExprColumnContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#caseExpr.
    def visitCaseExpr(self, ctx: HiveParser.CaseExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprTernaryOp.
    def visitColumnExprTernaryOp(self, ctx: HiveParser.ColumnExprTernaryOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprAlias.
    def visitColumnExprAlias(self, ctx: HiveParser.ColumnExprAliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprExtract.
    def visitColumnExprExtract(self, ctx: HiveParser.ColumnExprExtractContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprNegate.
    def visitColumnExprNegate(self, ctx: HiveParser.ColumnExprNegateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprSubquery.
    def visitColumnExprSubquery(self, ctx: HiveParser.ColumnExprSubqueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprLiteral.
    def visitColumnExprLiteral(self, ctx: HiveParser.ColumnExprLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprArray.
    def visitColumnExprArray(self, ctx: HiveParser.ColumnExprArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprSubstring.
    def visitColumnExprSubstring(self, ctx: HiveParser.ColumnExprSubstringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprCast.
    def visitColumnExprCast(self, ctx: HiveParser.ColumnExprCastContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprMultiIfExpr.
    def visitColumnExprMultiIfExpr(self, ctx: HiveParser.ColumnExprMultiIfExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprOr.
    def visitColumnExprOr(self, ctx: HiveParser.ColumnExprOrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnTypeDefinition.
    def visitColumnTypeDefinition(self, ctx: HiveParser.ColumnTypeDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprPowFunction.
    def visitColumnExprPowFunction(self, ctx: HiveParser.ColumnExprPowFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprPrecedence1.
    def visitColumnExprPrecedence1(self, ctx: HiveParser.ColumnExprPrecedence1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprBinaryCast.
    def visitColumnExprBinaryCast(self, ctx: HiveParser.ColumnExprBinaryCastContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprPrecedence2.
    def visitColumnExprPrecedence2(self, ctx: HiveParser.ColumnExprPrecedence2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprPrecedence3.
    def visitColumnExprPrecedence3(self, ctx: HiveParser.ColumnExprPrecedence3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprInterval.
    def visitColumnExprInterval(self, ctx: HiveParser.ColumnExprIntervalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprIsNull.
    def visitColumnExprIsNull(self, ctx: HiveParser.ColumnExprIsNullContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprIsTrue.
    def visitColumnExprIsTrue(self, ctx: HiveParser.ColumnExprIsTrueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprTrim.
    def visitColumnExprTrim(self, ctx: HiveParser.ColumnExprTrimContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprTuple.
    def visitColumnExprTuple(self, ctx: HiveParser.ColumnExprTupleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprArrayAccess.
    def visitColumnExprArrayAccess(self, ctx: HiveParser.ColumnExprArrayAccessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprBetween.
    def visitColumnExprBetween(self, ctx: HiveParser.ColumnExprBetweenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprParens.
    def visitColumnExprParens(self, ctx: HiveParser.ColumnExprParensContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprTimestamp.
    def visitColumnExprTimestamp(self, ctx: HiveParser.ColumnExprTimestampContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprAggFunction.
    def visitColumnExprAggFunction(self, ctx: HiveParser.ColumnExprAggFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprIfExpr.
    def visitColumnExprIfExpr(self, ctx: HiveParser.ColumnExprIfExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprAliasSubquery.
    def visitColumnExprAliasSubquery(self, ctx: HiveParser.ColumnExprAliasSubqueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprAnd.
    def visitColumnExprAnd(self, ctx: HiveParser.ColumnExprAndContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprTupleAccess.
    def visitColumnExprTupleAccess(self, ctx: HiveParser.ColumnExprTupleAccessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprCase.
    def visitColumnExprCase(self, ctx: HiveParser.ColumnExprCaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprSumCaseFunction.
    def visitColumnExprSumCaseFunction(self, ctx: HiveParser.ColumnExprSumCaseFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprDate.
    def visitColumnExprDate(self, ctx: HiveParser.ColumnExprDateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprNot.
    def visitColumnExprNot(self, ctx: HiveParser.ColumnExprNotContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprIdentifier.
    def visitColumnExprIdentifier(self, ctx: HiveParser.ColumnExprIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprFunction.
    def visitColumnExprFunction(self, ctx: HiveParser.ColumnExprFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnExprAsterisk.
    def visitColumnExprAsterisk(self, ctx: HiveParser.ColumnExprAsteriskContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#ColumnQuoteExpr.
    def visitColumnQuoteExpr(self, ctx: HiveParser.ColumnQuoteExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnArgList.
    def visitColumnArgList(self, ctx: HiveParser.ColumnArgListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnArgExpr.
    def visitColumnArgExpr(self, ctx: HiveParser.ColumnArgExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnLambdaExpr.
    def visitColumnLambdaExpr(self, ctx: HiveParser.ColumnLambdaExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#columnIdentifier.
    def visitColumnIdentifier(self, ctx: HiveParser.ColumnIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#nestedIdentifier.
    def visitNestedIdentifier(self, ctx: HiveParser.NestedIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#TableExprIdentifier.
    def visitTableExprIdentifier(self, ctx: HiveParser.TableExprIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#TableExprSubquery.
    def visitTableExprSubquery(self, ctx: HiveParser.TableExprSubqueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#TableExprAlias.
    def visitTableExprAlias(self, ctx: HiveParser.TableExprAliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#TableExprFunction.
    def visitTableExprFunction(self, ctx: HiveParser.TableExprFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#tableFunctionExpr.
    def visitTableFunctionExpr(self, ctx: HiveParser.TableFunctionExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#tableIdentifier.
    def visitTableIdentifier(self, ctx: HiveParser.TableIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#tableArgList.
    def visitTableArgList(self, ctx: HiveParser.TableArgListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#tableArgExpr.
    def visitTableArgExpr(self, ctx: HiveParser.TableArgExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#databaseIdentifier.
    def visitDatabaseIdentifier(self, ctx: HiveParser.DatabaseIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#floatingLiteral.
    def visitFloatingLiteral(self, ctx: HiveParser.FloatingLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#numberLiteral.
    def visitNumberLiteral(self, ctx: HiveParser.NumberLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#numliteral.
    def visitNumliteral(self, ctx: HiveParser.NumliteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#stringliteral.
    def visitStringliteral(self, ctx: HiveParser.StringliteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#nullliteral.
    def visitNullliteral(self, ctx: HiveParser.NullliteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#interval.
    def visitInterval(self, ctx: HiveParser.IntervalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#aggregateFunctionName.
    def visitAggregateFunctionName(self, ctx: HiveParser.AggregateFunctionNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#decimalTypeName.
    def visitDecimalTypeName(self, ctx: HiveParser.DecimalTypeNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#tupleOrArrayName.
    def visitTupleOrArrayName(self, ctx: HiveParser.TupleOrArrayNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#keyword.
    def visitKeyword(self, ctx: HiveParser.KeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#keywordForAlias.
    def visitKeywordForAlias(self, ctx: HiveParser.KeywordForAliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#alias.
    def visitAlias(self, ctx: HiveParser.AliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#identifier.
    def visitIdentifier(self, ctx: HiveParser.IdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#identifierOrNull.
    def visitIdentifierOrNull(self, ctx: HiveParser.IdentifierOrNullContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HiveParser#enumValue.
    def visitEnumValue(self, ctx: HiveParser.EnumValueContext):
        return self.visitChildren(ctx)


del HiveParser
