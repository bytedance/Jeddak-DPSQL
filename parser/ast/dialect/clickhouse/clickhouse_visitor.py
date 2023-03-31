# Generated from ClickHouse.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .clickhouse_parser import ClickHouseParser
else:
    from ClickHouseParser import ClickHouseParser

# This class defines a complete generic visitor for a parse tree produced by ClickHouseParser.

class ClickHouseVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ClickHouseParser#query.
    def visitQuery(self, ctx:ClickHouseParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#selectUnionStmt.
    def visitSelectUnionStmt(self, ctx:ClickHouseParser.SelectUnionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#StmtUnionAll.
    def visitStmtUnionAll(self, ctx:ClickHouseParser.StmtUnionAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#StmtUnionDistinct.
    def visitStmtUnionDistinct(self, ctx:ClickHouseParser.StmtUnionDistinctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#StmtUnion.
    def visitStmtUnion(self, ctx:ClickHouseParser.StmtUnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#selectStmtWithParens.
    def visitSelectStmtWithParens(self, ctx:ClickHouseParser.SelectStmtWithParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#selectStmt.
    def visitSelectStmt(self, ctx:ClickHouseParser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#formatClause.
    def visitFormatClause(self, ctx:ClickHouseParser.FormatClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#selectClause.
    def visitSelectClause(self, ctx:ClickHouseParser.SelectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#withClause.
    def visitWithClause(self, ctx:ClickHouseParser.WithClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#topClause.
    def visitTopClause(self, ctx:ClickHouseParser.TopClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#fromClause.
    def visitFromClause(self, ctx:ClickHouseParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#arrayJoinClause.
    def visitArrayJoinClause(self, ctx:ClickHouseParser.ArrayJoinClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#prewhereClause.
    def visitPrewhereClause(self, ctx:ClickHouseParser.PrewhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#whereClause.
    def visitWhereClause(self, ctx:ClickHouseParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#GroupFrontCr.
    def visitGroupFrontCr(self, ctx:ClickHouseParser.GroupFrontCrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#GroupNoFrontCr.
    def visitGroupNoFrontCr(self, ctx:ClickHouseParser.GroupNoFrontCrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#havingClause.
    def visitHavingClause(self, ctx:ClickHouseParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#orderByClause.
    def visitOrderByClause(self, ctx:ClickHouseParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#limitByClause.
    def visitLimitByClause(self, ctx:ClickHouseParser.LimitByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#limitClause.
    def visitLimitClause(self, ctx:ClickHouseParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tealimitClause.
    def visitTealimitClause(self, ctx:ClickHouseParser.TealimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#settingsClause.
    def visitSettingsClause(self, ctx:ClickHouseParser.SettingsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#GroupWithCube.
    def visitGroupWithCube(self, ctx:ClickHouseParser.GroupWithCubeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#GroupWithRollup.
    def visitGroupWithRollup(self, ctx:ClickHouseParser.GroupWithRollupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#GroupWithTotals.
    def visitGroupWithTotals(self, ctx:ClickHouseParser.GroupWithTotalsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinExprOp.
    def visitJoinExprOp(self, ctx:ClickHouseParser.JoinExprOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinExprTable.
    def visitJoinExprTable(self, ctx:ClickHouseParser.JoinExprTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinExprParens.
    def visitJoinExprParens(self, ctx:ClickHouseParser.JoinExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinExprCrossOp.
    def visitJoinExprCrossOp(self, ctx:ClickHouseParser.JoinExprCrossOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpInner1.
    def visitJoinOpInner1(self, ctx:ClickHouseParser.JoinOpInner1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpInner2.
    def visitJoinOpInner2(self, ctx:ClickHouseParser.JoinOpInner2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpInner3.
    def visitJoinOpInner3(self, ctx:ClickHouseParser.JoinOpInner3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpLeftRight1.
    def visitJoinOpLeftRight1(self, ctx:ClickHouseParser.JoinOpLeftRight1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpLeftRight2.
    def visitJoinOpLeftRight2(self, ctx:ClickHouseParser.JoinOpLeftRight2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpFull1.
    def visitJoinOpFull1(self, ctx:ClickHouseParser.JoinOpFull1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#JoinOpFull2.
    def visitJoinOpFull2(self, ctx:ClickHouseParser.JoinOpFull2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#joinOpCross.
    def visitJoinOpCross(self, ctx:ClickHouseParser.JoinOpCrossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#joinConstraintClause.
    def visitJoinConstraintClause(self, ctx:ClickHouseParser.JoinConstraintClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#sampleClause.
    def visitSampleClause(self, ctx:ClickHouseParser.SampleClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#limitExpr.
    def visitLimitExpr(self, ctx:ClickHouseParser.LimitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#orderExprList.
    def visitOrderExprList(self, ctx:ClickHouseParser.OrderExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#orderExpr.
    def visitOrderExpr(self, ctx:ClickHouseParser.OrderExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ratioExpr.
    def visitRatioExpr(self, ctx:ClickHouseParser.RatioExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#settingExprList.
    def visitSettingExprList(self, ctx:ClickHouseParser.SettingExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#settingExpr.
    def visitSettingExpr(self, ctx:ClickHouseParser.SettingExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeExprSimple.
    def visitColumnTypeExprSimple(self, ctx:ClickHouseParser.ColumnTypeExprSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeExprNested.
    def visitColumnTypeExprNested(self, ctx:ClickHouseParser.ColumnTypeExprNestedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeExprEnum.
    def visitColumnTypeExprEnum(self, ctx:ClickHouseParser.ColumnTypeExprEnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeExprComplex.
    def visitColumnTypeExprComplex(self, ctx:ClickHouseParser.ColumnTypeExprComplexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeDecimal.
    def visitColumnTypeDecimal(self, ctx:ClickHouseParser.ColumnTypeDecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeExprParam.
    def visitColumnTypeExprParam(self, ctx:ClickHouseParser.ColumnTypeExprParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnDefinitionExpr.
    def visitColumnDefinitionExpr(self, ctx:ClickHouseParser.ColumnDefinitionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnExprList.
    def visitColumnExprList(self, ctx:ClickHouseParser.ColumnExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnExprWhen.
    def visitColumnExprWhen(self, ctx:ClickHouseParser.ColumnExprWhenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnsExprAsterisk.
    def visitColumnsExprAsterisk(self, ctx:ClickHouseParser.ColumnsExprAsteriskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnsExprSubquery.
    def visitColumnsExprSubquery(self, ctx:ClickHouseParser.ColumnsExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnsExprColumn.
    def visitColumnsExprColumn(self, ctx:ClickHouseParser.ColumnsExprColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#caseExpr.
    def visitCaseExpr(self, ctx:ClickHouseParser.CaseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprTernaryOp.
    def visitColumnExprTernaryOp(self, ctx:ClickHouseParser.ColumnExprTernaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprAlias.
    def visitColumnExprAlias(self, ctx:ClickHouseParser.ColumnExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprExtract.
    def visitColumnExprExtract(self, ctx:ClickHouseParser.ColumnExprExtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprNegate.
    def visitColumnExprNegate(self, ctx:ClickHouseParser.ColumnExprNegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprSubquery.
    def visitColumnExprSubquery(self, ctx:ClickHouseParser.ColumnExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprLiteral.
    def visitColumnExprLiteral(self, ctx:ClickHouseParser.ColumnExprLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprArray.
    def visitColumnExprArray(self, ctx:ClickHouseParser.ColumnExprArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprSubstring.
    def visitColumnExprSubstring(self, ctx:ClickHouseParser.ColumnExprSubstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprCast.
    def visitColumnExprCast(self, ctx:ClickHouseParser.ColumnExprCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprMultiIfExpr.
    def visitColumnExprMultiIfExpr(self, ctx:ClickHouseParser.ColumnExprMultiIfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprOr.
    def visitColumnExprOr(self, ctx:ClickHouseParser.ColumnExprOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnTypeDefinition.
    def visitColumnTypeDefinition(self, ctx:ClickHouseParser.ColumnTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprPowFunction.
    def visitColumnExprPowFunction(self, ctx:ClickHouseParser.ColumnExprPowFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprPrecedence1.
    def visitColumnExprPrecedence1(self, ctx:ClickHouseParser.ColumnExprPrecedence1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprPrecedence2.
    def visitColumnExprPrecedence2(self, ctx:ClickHouseParser.ColumnExprPrecedence2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprPrecedence3.
    def visitColumnExprPrecedence3(self, ctx:ClickHouseParser.ColumnExprPrecedence3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprInterval.
    def visitColumnExprInterval(self, ctx:ClickHouseParser.ColumnExprIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprIsNull.
    def visitColumnExprIsNull(self, ctx:ClickHouseParser.ColumnExprIsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprTrim.
    def visitColumnExprTrim(self, ctx:ClickHouseParser.ColumnExprTrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprTuple.
    def visitColumnExprTuple(self, ctx:ClickHouseParser.ColumnExprTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprArrayAccess.
    def visitColumnExprArrayAccess(self, ctx:ClickHouseParser.ColumnExprArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprBetween.
    def visitColumnExprBetween(self, ctx:ClickHouseParser.ColumnExprBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprParens.
    def visitColumnExprParens(self, ctx:ClickHouseParser.ColumnExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprTimestamp.
    def visitColumnExprTimestamp(self, ctx:ClickHouseParser.ColumnExprTimestampContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprAggFunction.
    def visitColumnExprAggFunction(self, ctx:ClickHouseParser.ColumnExprAggFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprIfExpr.
    def visitColumnExprIfExpr(self, ctx:ClickHouseParser.ColumnExprIfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprAliasSubquery.
    def visitColumnExprAliasSubquery(self, ctx:ClickHouseParser.ColumnExprAliasSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprAnd.
    def visitColumnExprAnd(self, ctx:ClickHouseParser.ColumnExprAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprTupleAccess.
    def visitColumnExprTupleAccess(self, ctx:ClickHouseParser.ColumnExprTupleAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprCase.
    def visitColumnExprCase(self, ctx:ClickHouseParser.ColumnExprCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprSumCaseFunction.
    def visitColumnExprSumCaseFunction(self, ctx:ClickHouseParser.ColumnExprSumCaseFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprDate.
    def visitColumnExprDate(self, ctx:ClickHouseParser.ColumnExprDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprNot.
    def visitColumnExprNot(self, ctx:ClickHouseParser.ColumnExprNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprIdentifier.
    def visitColumnExprIdentifier(self, ctx:ClickHouseParser.ColumnExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprFunction.
    def visitColumnExprFunction(self, ctx:ClickHouseParser.ColumnExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnExprAsterisk.
    def visitColumnExprAsterisk(self, ctx:ClickHouseParser.ColumnExprAsteriskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#ColumnQuoteExpr.
    def visitColumnQuoteExpr(self, ctx:ClickHouseParser.ColumnQuoteExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnArgList.
    def visitColumnArgList(self, ctx:ClickHouseParser.ColumnArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnArgExpr.
    def visitColumnArgExpr(self, ctx:ClickHouseParser.ColumnArgExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnLambdaExpr.
    def visitColumnLambdaExpr(self, ctx:ClickHouseParser.ColumnLambdaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#columnIdentifier.
    def visitColumnIdentifier(self, ctx:ClickHouseParser.ColumnIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#nestedIdentifier.
    def visitNestedIdentifier(self, ctx:ClickHouseParser.NestedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#TableExprIdentifier.
    def visitTableExprIdentifier(self, ctx:ClickHouseParser.TableExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#TableExprSubquery.
    def visitTableExprSubquery(self, ctx:ClickHouseParser.TableExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#TableExprAlias.
    def visitTableExprAlias(self, ctx:ClickHouseParser.TableExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#TableFushionMerge.
    def visitTableFushionMerge(self, ctx:ClickHouseParser.TableFushionMergeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#TableExprFunction.
    def visitTableExprFunction(self, ctx:ClickHouseParser.TableExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#fushionMerge.
    def visitFushionMerge(self, ctx:ClickHouseParser.FushionMergeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tableFunctionExpr.
    def visitTableFunctionExpr(self, ctx:ClickHouseParser.TableFunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tableIdentifier.
    def visitTableIdentifier(self, ctx:ClickHouseParser.TableIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tableArgList.
    def visitTableArgList(self, ctx:ClickHouseParser.TableArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tableArgExpr.
    def visitTableArgExpr(self, ctx:ClickHouseParser.TableArgExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#databaseIdentifier.
    def visitDatabaseIdentifier(self, ctx:ClickHouseParser.DatabaseIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#floatingLiteral.
    def visitFloatingLiteral(self, ctx:ClickHouseParser.FloatingLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#numberLiteral.
    def visitNumberLiteral(self, ctx:ClickHouseParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#numliteral.
    def visitNumliteral(self, ctx:ClickHouseParser.NumliteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#stringliteral.
    def visitStringliteral(self, ctx:ClickHouseParser.StringliteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#nullliteral.
    def visitNullliteral(self, ctx:ClickHouseParser.NullliteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#interval.
    def visitInterval(self, ctx:ClickHouseParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#aggregateFunctionName.
    def visitAggregateFunctionName(self, ctx:ClickHouseParser.AggregateFunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#decimalTypeName.
    def visitDecimalTypeName(self, ctx:ClickHouseParser.DecimalTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#tupleOrArrayName.
    def visitTupleOrArrayName(self, ctx:ClickHouseParser.TupleOrArrayNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#keyword.
    def visitKeyword(self, ctx:ClickHouseParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#keywordForAlias.
    def visitKeywordForAlias(self, ctx:ClickHouseParser.KeywordForAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#alias.
    def visitAlias(self, ctx:ClickHouseParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#identifier.
    def visitIdentifier(self, ctx:ClickHouseParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#identifierOrNull.
    def visitIdentifierOrNull(self, ctx:ClickHouseParser.IdentifierOrNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClickHouseParser#enumValue.
    def visitEnumValue(self, ctx:ClickHouseParser.EnumValueContext):
        return self.visitChildren(ctx)



del ClickHouseParser