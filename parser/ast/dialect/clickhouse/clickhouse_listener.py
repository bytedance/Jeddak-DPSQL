# Generated from ClickHouse.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .clickhouse_parser import ClickHouseParser
else:
    from ClickHouseParser import ClickHouseParser

# This class defines a complete listener for a parse tree produced by ClickHouseParser.
class ClickHouseListener(ParseTreeListener):

    # Enter a parse tree produced by ClickHouseParser#query.
    def enterQuery(self, ctx:ClickHouseParser.QueryContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#query.
    def exitQuery(self, ctx:ClickHouseParser.QueryContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#selectUnionStmt.
    def enterSelectUnionStmt(self, ctx:ClickHouseParser.SelectUnionStmtContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#selectUnionStmt.
    def exitSelectUnionStmt(self, ctx:ClickHouseParser.SelectUnionStmtContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#StmtUnionAll.
    def enterStmtUnionAll(self, ctx:ClickHouseParser.StmtUnionAllContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#StmtUnionAll.
    def exitStmtUnionAll(self, ctx:ClickHouseParser.StmtUnionAllContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#StmtUnionDistinct.
    def enterStmtUnionDistinct(self, ctx:ClickHouseParser.StmtUnionDistinctContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#StmtUnionDistinct.
    def exitStmtUnionDistinct(self, ctx:ClickHouseParser.StmtUnionDistinctContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#StmtUnion.
    def enterStmtUnion(self, ctx:ClickHouseParser.StmtUnionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#StmtUnion.
    def exitStmtUnion(self, ctx:ClickHouseParser.StmtUnionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#selectStmtWithParens.
    def enterSelectStmtWithParens(self, ctx:ClickHouseParser.SelectStmtWithParensContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#selectStmtWithParens.
    def exitSelectStmtWithParens(self, ctx:ClickHouseParser.SelectStmtWithParensContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#selectStmt.
    def enterSelectStmt(self, ctx:ClickHouseParser.SelectStmtContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#selectStmt.
    def exitSelectStmt(self, ctx:ClickHouseParser.SelectStmtContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#formatClause.
    def enterFormatClause(self, ctx:ClickHouseParser.FormatClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#formatClause.
    def exitFormatClause(self, ctx:ClickHouseParser.FormatClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#selectClause.
    def enterSelectClause(self, ctx:ClickHouseParser.SelectClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#selectClause.
    def exitSelectClause(self, ctx:ClickHouseParser.SelectClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#withClause.
    def enterWithClause(self, ctx:ClickHouseParser.WithClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#withClause.
    def exitWithClause(self, ctx:ClickHouseParser.WithClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#topClause.
    def enterTopClause(self, ctx:ClickHouseParser.TopClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#topClause.
    def exitTopClause(self, ctx:ClickHouseParser.TopClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#fromClause.
    def enterFromClause(self, ctx:ClickHouseParser.FromClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#fromClause.
    def exitFromClause(self, ctx:ClickHouseParser.FromClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#arrayJoinClause.
    def enterArrayJoinClause(self, ctx:ClickHouseParser.ArrayJoinClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#arrayJoinClause.
    def exitArrayJoinClause(self, ctx:ClickHouseParser.ArrayJoinClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#prewhereClause.
    def enterPrewhereClause(self, ctx:ClickHouseParser.PrewhereClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#prewhereClause.
    def exitPrewhereClause(self, ctx:ClickHouseParser.PrewhereClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#whereClause.
    def enterWhereClause(self, ctx:ClickHouseParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#whereClause.
    def exitWhereClause(self, ctx:ClickHouseParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#GroupFrontCr.
    def enterGroupFrontCr(self, ctx:ClickHouseParser.GroupFrontCrContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#GroupFrontCr.
    def exitGroupFrontCr(self, ctx:ClickHouseParser.GroupFrontCrContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#GroupNoFrontCr.
    def enterGroupNoFrontCr(self, ctx:ClickHouseParser.GroupNoFrontCrContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#GroupNoFrontCr.
    def exitGroupNoFrontCr(self, ctx:ClickHouseParser.GroupNoFrontCrContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#havingClause.
    def enterHavingClause(self, ctx:ClickHouseParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#havingClause.
    def exitHavingClause(self, ctx:ClickHouseParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#orderByClause.
    def enterOrderByClause(self, ctx:ClickHouseParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#orderByClause.
    def exitOrderByClause(self, ctx:ClickHouseParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#limitByClause.
    def enterLimitByClause(self, ctx:ClickHouseParser.LimitByClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#limitByClause.
    def exitLimitByClause(self, ctx:ClickHouseParser.LimitByClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#limitClause.
    def enterLimitClause(self, ctx:ClickHouseParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#limitClause.
    def exitLimitClause(self, ctx:ClickHouseParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tealimitClause.
    def enterTealimitClause(self, ctx:ClickHouseParser.TealimitClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tealimitClause.
    def exitTealimitClause(self, ctx:ClickHouseParser.TealimitClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#settingsClause.
    def enterSettingsClause(self, ctx:ClickHouseParser.SettingsClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#settingsClause.
    def exitSettingsClause(self, ctx:ClickHouseParser.SettingsClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#GroupWithCube.
    def enterGroupWithCube(self, ctx:ClickHouseParser.GroupWithCubeContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#GroupWithCube.
    def exitGroupWithCube(self, ctx:ClickHouseParser.GroupWithCubeContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#GroupWithRollup.
    def enterGroupWithRollup(self, ctx:ClickHouseParser.GroupWithRollupContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#GroupWithRollup.
    def exitGroupWithRollup(self, ctx:ClickHouseParser.GroupWithRollupContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#GroupWithTotals.
    def enterGroupWithTotals(self, ctx:ClickHouseParser.GroupWithTotalsContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#GroupWithTotals.
    def exitGroupWithTotals(self, ctx:ClickHouseParser.GroupWithTotalsContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinExprOp.
    def enterJoinExprOp(self, ctx:ClickHouseParser.JoinExprOpContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinExprOp.
    def exitJoinExprOp(self, ctx:ClickHouseParser.JoinExprOpContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinExprTable.
    def enterJoinExprTable(self, ctx:ClickHouseParser.JoinExprTableContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinExprTable.
    def exitJoinExprTable(self, ctx:ClickHouseParser.JoinExprTableContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinExprParens.
    def enterJoinExprParens(self, ctx:ClickHouseParser.JoinExprParensContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinExprParens.
    def exitJoinExprParens(self, ctx:ClickHouseParser.JoinExprParensContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinExprCrossOp.
    def enterJoinExprCrossOp(self, ctx:ClickHouseParser.JoinExprCrossOpContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinExprCrossOp.
    def exitJoinExprCrossOp(self, ctx:ClickHouseParser.JoinExprCrossOpContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpInner1.
    def enterJoinOpInner1(self, ctx:ClickHouseParser.JoinOpInner1Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpInner1.
    def exitJoinOpInner1(self, ctx:ClickHouseParser.JoinOpInner1Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpInner2.
    def enterJoinOpInner2(self, ctx:ClickHouseParser.JoinOpInner2Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpInner2.
    def exitJoinOpInner2(self, ctx:ClickHouseParser.JoinOpInner2Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpInner3.
    def enterJoinOpInner3(self, ctx:ClickHouseParser.JoinOpInner3Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpInner3.
    def exitJoinOpInner3(self, ctx:ClickHouseParser.JoinOpInner3Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpLeftRight1.
    def enterJoinOpLeftRight1(self, ctx:ClickHouseParser.JoinOpLeftRight1Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpLeftRight1.
    def exitJoinOpLeftRight1(self, ctx:ClickHouseParser.JoinOpLeftRight1Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpLeftRight2.
    def enterJoinOpLeftRight2(self, ctx:ClickHouseParser.JoinOpLeftRight2Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpLeftRight2.
    def exitJoinOpLeftRight2(self, ctx:ClickHouseParser.JoinOpLeftRight2Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpFull1.
    def enterJoinOpFull1(self, ctx:ClickHouseParser.JoinOpFull1Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpFull1.
    def exitJoinOpFull1(self, ctx:ClickHouseParser.JoinOpFull1Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#JoinOpFull2.
    def enterJoinOpFull2(self, ctx:ClickHouseParser.JoinOpFull2Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#JoinOpFull2.
    def exitJoinOpFull2(self, ctx:ClickHouseParser.JoinOpFull2Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#joinOpCross.
    def enterJoinOpCross(self, ctx:ClickHouseParser.JoinOpCrossContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#joinOpCross.
    def exitJoinOpCross(self, ctx:ClickHouseParser.JoinOpCrossContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#joinConstraintClause.
    def enterJoinConstraintClause(self, ctx:ClickHouseParser.JoinConstraintClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#joinConstraintClause.
    def exitJoinConstraintClause(self, ctx:ClickHouseParser.JoinConstraintClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#sampleClause.
    def enterSampleClause(self, ctx:ClickHouseParser.SampleClauseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#sampleClause.
    def exitSampleClause(self, ctx:ClickHouseParser.SampleClauseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#limitExpr.
    def enterLimitExpr(self, ctx:ClickHouseParser.LimitExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#limitExpr.
    def exitLimitExpr(self, ctx:ClickHouseParser.LimitExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#orderExprList.
    def enterOrderExprList(self, ctx:ClickHouseParser.OrderExprListContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#orderExprList.
    def exitOrderExprList(self, ctx:ClickHouseParser.OrderExprListContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#orderExpr.
    def enterOrderExpr(self, ctx:ClickHouseParser.OrderExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#orderExpr.
    def exitOrderExpr(self, ctx:ClickHouseParser.OrderExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ratioExpr.
    def enterRatioExpr(self, ctx:ClickHouseParser.RatioExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ratioExpr.
    def exitRatioExpr(self, ctx:ClickHouseParser.RatioExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#settingExprList.
    def enterSettingExprList(self, ctx:ClickHouseParser.SettingExprListContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#settingExprList.
    def exitSettingExprList(self, ctx:ClickHouseParser.SettingExprListContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#settingExpr.
    def enterSettingExpr(self, ctx:ClickHouseParser.SettingExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#settingExpr.
    def exitSettingExpr(self, ctx:ClickHouseParser.SettingExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeExprSimple.
    def enterColumnTypeExprSimple(self, ctx:ClickHouseParser.ColumnTypeExprSimpleContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeExprSimple.
    def exitColumnTypeExprSimple(self, ctx:ClickHouseParser.ColumnTypeExprSimpleContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeExprNested.
    def enterColumnTypeExprNested(self, ctx:ClickHouseParser.ColumnTypeExprNestedContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeExprNested.
    def exitColumnTypeExprNested(self, ctx:ClickHouseParser.ColumnTypeExprNestedContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeExprEnum.
    def enterColumnTypeExprEnum(self, ctx:ClickHouseParser.ColumnTypeExprEnumContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeExprEnum.
    def exitColumnTypeExprEnum(self, ctx:ClickHouseParser.ColumnTypeExprEnumContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeExprComplex.
    def enterColumnTypeExprComplex(self, ctx:ClickHouseParser.ColumnTypeExprComplexContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeExprComplex.
    def exitColumnTypeExprComplex(self, ctx:ClickHouseParser.ColumnTypeExprComplexContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeDecimal.
    def enterColumnTypeDecimal(self, ctx:ClickHouseParser.ColumnTypeDecimalContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeDecimal.
    def exitColumnTypeDecimal(self, ctx:ClickHouseParser.ColumnTypeDecimalContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeExprParam.
    def enterColumnTypeExprParam(self, ctx:ClickHouseParser.ColumnTypeExprParamContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeExprParam.
    def exitColumnTypeExprParam(self, ctx:ClickHouseParser.ColumnTypeExprParamContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnDefinitionExpr.
    def enterColumnDefinitionExpr(self, ctx:ClickHouseParser.ColumnDefinitionExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnDefinitionExpr.
    def exitColumnDefinitionExpr(self, ctx:ClickHouseParser.ColumnDefinitionExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnExprList.
    def enterColumnExprList(self, ctx:ClickHouseParser.ColumnExprListContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnExprList.
    def exitColumnExprList(self, ctx:ClickHouseParser.ColumnExprListContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnExprWhen.
    def enterColumnExprWhen(self, ctx:ClickHouseParser.ColumnExprWhenContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnExprWhen.
    def exitColumnExprWhen(self, ctx:ClickHouseParser.ColumnExprWhenContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnsExprAsterisk.
    def enterColumnsExprAsterisk(self, ctx:ClickHouseParser.ColumnsExprAsteriskContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnsExprAsterisk.
    def exitColumnsExprAsterisk(self, ctx:ClickHouseParser.ColumnsExprAsteriskContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnsExprSubquery.
    def enterColumnsExprSubquery(self, ctx:ClickHouseParser.ColumnsExprSubqueryContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnsExprSubquery.
    def exitColumnsExprSubquery(self, ctx:ClickHouseParser.ColumnsExprSubqueryContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnsExprColumn.
    def enterColumnsExprColumn(self, ctx:ClickHouseParser.ColumnsExprColumnContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnsExprColumn.
    def exitColumnsExprColumn(self, ctx:ClickHouseParser.ColumnsExprColumnContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#caseExpr.
    def enterCaseExpr(self, ctx:ClickHouseParser.CaseExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#caseExpr.
    def exitCaseExpr(self, ctx:ClickHouseParser.CaseExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprTernaryOp.
    def enterColumnExprTernaryOp(self, ctx:ClickHouseParser.ColumnExprTernaryOpContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprTernaryOp.
    def exitColumnExprTernaryOp(self, ctx:ClickHouseParser.ColumnExprTernaryOpContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprAlias.
    def enterColumnExprAlias(self, ctx:ClickHouseParser.ColumnExprAliasContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprAlias.
    def exitColumnExprAlias(self, ctx:ClickHouseParser.ColumnExprAliasContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprExtract.
    def enterColumnExprExtract(self, ctx:ClickHouseParser.ColumnExprExtractContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprExtract.
    def exitColumnExprExtract(self, ctx:ClickHouseParser.ColumnExprExtractContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprNegate.
    def enterColumnExprNegate(self, ctx:ClickHouseParser.ColumnExprNegateContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprNegate.
    def exitColumnExprNegate(self, ctx:ClickHouseParser.ColumnExprNegateContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprSubquery.
    def enterColumnExprSubquery(self, ctx:ClickHouseParser.ColumnExprSubqueryContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprSubquery.
    def exitColumnExprSubquery(self, ctx:ClickHouseParser.ColumnExprSubqueryContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprLiteral.
    def enterColumnExprLiteral(self, ctx:ClickHouseParser.ColumnExprLiteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprLiteral.
    def exitColumnExprLiteral(self, ctx:ClickHouseParser.ColumnExprLiteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprArray.
    def enterColumnExprArray(self, ctx:ClickHouseParser.ColumnExprArrayContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprArray.
    def exitColumnExprArray(self, ctx:ClickHouseParser.ColumnExprArrayContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprSubstring.
    def enterColumnExprSubstring(self, ctx:ClickHouseParser.ColumnExprSubstringContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprSubstring.
    def exitColumnExprSubstring(self, ctx:ClickHouseParser.ColumnExprSubstringContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprCast.
    def enterColumnExprCast(self, ctx:ClickHouseParser.ColumnExprCastContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprCast.
    def exitColumnExprCast(self, ctx:ClickHouseParser.ColumnExprCastContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprMultiIfExpr.
    def enterColumnExprMultiIfExpr(self, ctx:ClickHouseParser.ColumnExprMultiIfExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprMultiIfExpr.
    def exitColumnExprMultiIfExpr(self, ctx:ClickHouseParser.ColumnExprMultiIfExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprOr.
    def enterColumnExprOr(self, ctx:ClickHouseParser.ColumnExprOrContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprOr.
    def exitColumnExprOr(self, ctx:ClickHouseParser.ColumnExprOrContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnTypeDefinition.
    def enterColumnTypeDefinition(self, ctx:ClickHouseParser.ColumnTypeDefinitionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnTypeDefinition.
    def exitColumnTypeDefinition(self, ctx:ClickHouseParser.ColumnTypeDefinitionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprPowFunction.
    def enterColumnExprPowFunction(self, ctx:ClickHouseParser.ColumnExprPowFunctionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprPowFunction.
    def exitColumnExprPowFunction(self, ctx:ClickHouseParser.ColumnExprPowFunctionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprPrecedence1.
    def enterColumnExprPrecedence1(self, ctx:ClickHouseParser.ColumnExprPrecedence1Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprPrecedence1.
    def exitColumnExprPrecedence1(self, ctx:ClickHouseParser.ColumnExprPrecedence1Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprPrecedence2.
    def enterColumnExprPrecedence2(self, ctx:ClickHouseParser.ColumnExprPrecedence2Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprPrecedence2.
    def exitColumnExprPrecedence2(self, ctx:ClickHouseParser.ColumnExprPrecedence2Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprPrecedence3.
    def enterColumnExprPrecedence3(self, ctx:ClickHouseParser.ColumnExprPrecedence3Context):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprPrecedence3.
    def exitColumnExprPrecedence3(self, ctx:ClickHouseParser.ColumnExprPrecedence3Context):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprInterval.
    def enterColumnExprInterval(self, ctx:ClickHouseParser.ColumnExprIntervalContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprInterval.
    def exitColumnExprInterval(self, ctx:ClickHouseParser.ColumnExprIntervalContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprIsNull.
    def enterColumnExprIsNull(self, ctx:ClickHouseParser.ColumnExprIsNullContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprIsNull.
    def exitColumnExprIsNull(self, ctx:ClickHouseParser.ColumnExprIsNullContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprTrim.
    def enterColumnExprTrim(self, ctx:ClickHouseParser.ColumnExprTrimContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprTrim.
    def exitColumnExprTrim(self, ctx:ClickHouseParser.ColumnExprTrimContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprTuple.
    def enterColumnExprTuple(self, ctx:ClickHouseParser.ColumnExprTupleContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprTuple.
    def exitColumnExprTuple(self, ctx:ClickHouseParser.ColumnExprTupleContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprArrayAccess.
    def enterColumnExprArrayAccess(self, ctx:ClickHouseParser.ColumnExprArrayAccessContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprArrayAccess.
    def exitColumnExprArrayAccess(self, ctx:ClickHouseParser.ColumnExprArrayAccessContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprBetween.
    def enterColumnExprBetween(self, ctx:ClickHouseParser.ColumnExprBetweenContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprBetween.
    def exitColumnExprBetween(self, ctx:ClickHouseParser.ColumnExprBetweenContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprParens.
    def enterColumnExprParens(self, ctx:ClickHouseParser.ColumnExprParensContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprParens.
    def exitColumnExprParens(self, ctx:ClickHouseParser.ColumnExprParensContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprTimestamp.
    def enterColumnExprTimestamp(self, ctx:ClickHouseParser.ColumnExprTimestampContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprTimestamp.
    def exitColumnExprTimestamp(self, ctx:ClickHouseParser.ColumnExprTimestampContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprAggFunction.
    def enterColumnExprAggFunction(self, ctx:ClickHouseParser.ColumnExprAggFunctionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprAggFunction.
    def exitColumnExprAggFunction(self, ctx:ClickHouseParser.ColumnExprAggFunctionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprIfExpr.
    def enterColumnExprIfExpr(self, ctx:ClickHouseParser.ColumnExprIfExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprIfExpr.
    def exitColumnExprIfExpr(self, ctx:ClickHouseParser.ColumnExprIfExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprAliasSubquery.
    def enterColumnExprAliasSubquery(self, ctx:ClickHouseParser.ColumnExprAliasSubqueryContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprAliasSubquery.
    def exitColumnExprAliasSubquery(self, ctx:ClickHouseParser.ColumnExprAliasSubqueryContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprAnd.
    def enterColumnExprAnd(self, ctx:ClickHouseParser.ColumnExprAndContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprAnd.
    def exitColumnExprAnd(self, ctx:ClickHouseParser.ColumnExprAndContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprTupleAccess.
    def enterColumnExprTupleAccess(self, ctx:ClickHouseParser.ColumnExprTupleAccessContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprTupleAccess.
    def exitColumnExprTupleAccess(self, ctx:ClickHouseParser.ColumnExprTupleAccessContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprCase.
    def enterColumnExprCase(self, ctx:ClickHouseParser.ColumnExprCaseContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprCase.
    def exitColumnExprCase(self, ctx:ClickHouseParser.ColumnExprCaseContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprSumCaseFunction.
    def enterColumnExprSumCaseFunction(self, ctx:ClickHouseParser.ColumnExprSumCaseFunctionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprSumCaseFunction.
    def exitColumnExprSumCaseFunction(self, ctx:ClickHouseParser.ColumnExprSumCaseFunctionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprDate.
    def enterColumnExprDate(self, ctx:ClickHouseParser.ColumnExprDateContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprDate.
    def exitColumnExprDate(self, ctx:ClickHouseParser.ColumnExprDateContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprNot.
    def enterColumnExprNot(self, ctx:ClickHouseParser.ColumnExprNotContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprNot.
    def exitColumnExprNot(self, ctx:ClickHouseParser.ColumnExprNotContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprIdentifier.
    def enterColumnExprIdentifier(self, ctx:ClickHouseParser.ColumnExprIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprIdentifier.
    def exitColumnExprIdentifier(self, ctx:ClickHouseParser.ColumnExprIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprFunction.
    def enterColumnExprFunction(self, ctx:ClickHouseParser.ColumnExprFunctionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprFunction.
    def exitColumnExprFunction(self, ctx:ClickHouseParser.ColumnExprFunctionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnExprAsterisk.
    def enterColumnExprAsterisk(self, ctx:ClickHouseParser.ColumnExprAsteriskContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnExprAsterisk.
    def exitColumnExprAsterisk(self, ctx:ClickHouseParser.ColumnExprAsteriskContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#ColumnQuoteExpr.
    def enterColumnQuoteExpr(self, ctx:ClickHouseParser.ColumnQuoteExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#ColumnQuoteExpr.
    def exitColumnQuoteExpr(self, ctx:ClickHouseParser.ColumnQuoteExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnArgList.
    def enterColumnArgList(self, ctx:ClickHouseParser.ColumnArgListContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnArgList.
    def exitColumnArgList(self, ctx:ClickHouseParser.ColumnArgListContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnArgExpr.
    def enterColumnArgExpr(self, ctx:ClickHouseParser.ColumnArgExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnArgExpr.
    def exitColumnArgExpr(self, ctx:ClickHouseParser.ColumnArgExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnLambdaExpr.
    def enterColumnLambdaExpr(self, ctx:ClickHouseParser.ColumnLambdaExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnLambdaExpr.
    def exitColumnLambdaExpr(self, ctx:ClickHouseParser.ColumnLambdaExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#columnIdentifier.
    def enterColumnIdentifier(self, ctx:ClickHouseParser.ColumnIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#columnIdentifier.
    def exitColumnIdentifier(self, ctx:ClickHouseParser.ColumnIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#nestedIdentifier.
    def enterNestedIdentifier(self, ctx:ClickHouseParser.NestedIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#nestedIdentifier.
    def exitNestedIdentifier(self, ctx:ClickHouseParser.NestedIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#TableExprIdentifier.
    def enterTableExprIdentifier(self, ctx:ClickHouseParser.TableExprIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#TableExprIdentifier.
    def exitTableExprIdentifier(self, ctx:ClickHouseParser.TableExprIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#TableExprSubquery.
    def enterTableExprSubquery(self, ctx:ClickHouseParser.TableExprSubqueryContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#TableExprSubquery.
    def exitTableExprSubquery(self, ctx:ClickHouseParser.TableExprSubqueryContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#TableExprAlias.
    def enterTableExprAlias(self, ctx:ClickHouseParser.TableExprAliasContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#TableExprAlias.
    def exitTableExprAlias(self, ctx:ClickHouseParser.TableExprAliasContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#TableFushionMerge.
    def enterTableFushionMerge(self, ctx:ClickHouseParser.TableFushionMergeContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#TableFushionMerge.
    def exitTableFushionMerge(self, ctx:ClickHouseParser.TableFushionMergeContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#TableExprFunction.
    def enterTableExprFunction(self, ctx:ClickHouseParser.TableExprFunctionContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#TableExprFunction.
    def exitTableExprFunction(self, ctx:ClickHouseParser.TableExprFunctionContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#fushionMerge.
    def enterFushionMerge(self, ctx:ClickHouseParser.FushionMergeContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#fushionMerge.
    def exitFushionMerge(self, ctx:ClickHouseParser.FushionMergeContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tableFunctionExpr.
    def enterTableFunctionExpr(self, ctx:ClickHouseParser.TableFunctionExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tableFunctionExpr.
    def exitTableFunctionExpr(self, ctx:ClickHouseParser.TableFunctionExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tableIdentifier.
    def enterTableIdentifier(self, ctx:ClickHouseParser.TableIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tableIdentifier.
    def exitTableIdentifier(self, ctx:ClickHouseParser.TableIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tableArgList.
    def enterTableArgList(self, ctx:ClickHouseParser.TableArgListContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tableArgList.
    def exitTableArgList(self, ctx:ClickHouseParser.TableArgListContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tableArgExpr.
    def enterTableArgExpr(self, ctx:ClickHouseParser.TableArgExprContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tableArgExpr.
    def exitTableArgExpr(self, ctx:ClickHouseParser.TableArgExprContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#databaseIdentifier.
    def enterDatabaseIdentifier(self, ctx:ClickHouseParser.DatabaseIdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#databaseIdentifier.
    def exitDatabaseIdentifier(self, ctx:ClickHouseParser.DatabaseIdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#floatingLiteral.
    def enterFloatingLiteral(self, ctx:ClickHouseParser.FloatingLiteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#floatingLiteral.
    def exitFloatingLiteral(self, ctx:ClickHouseParser.FloatingLiteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#numberLiteral.
    def enterNumberLiteral(self, ctx:ClickHouseParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#numberLiteral.
    def exitNumberLiteral(self, ctx:ClickHouseParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#numliteral.
    def enterNumliteral(self, ctx:ClickHouseParser.NumliteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#numliteral.
    def exitNumliteral(self, ctx:ClickHouseParser.NumliteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#stringliteral.
    def enterStringliteral(self, ctx:ClickHouseParser.StringliteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#stringliteral.
    def exitStringliteral(self, ctx:ClickHouseParser.StringliteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#nullliteral.
    def enterNullliteral(self, ctx:ClickHouseParser.NullliteralContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#nullliteral.
    def exitNullliteral(self, ctx:ClickHouseParser.NullliteralContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#interval.
    def enterInterval(self, ctx:ClickHouseParser.IntervalContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#interval.
    def exitInterval(self, ctx:ClickHouseParser.IntervalContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#aggregateFunctionName.
    def enterAggregateFunctionName(self, ctx:ClickHouseParser.AggregateFunctionNameContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#aggregateFunctionName.
    def exitAggregateFunctionName(self, ctx:ClickHouseParser.AggregateFunctionNameContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#decimalTypeName.
    def enterDecimalTypeName(self, ctx:ClickHouseParser.DecimalTypeNameContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#decimalTypeName.
    def exitDecimalTypeName(self, ctx:ClickHouseParser.DecimalTypeNameContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#tupleOrArrayName.
    def enterTupleOrArrayName(self, ctx:ClickHouseParser.TupleOrArrayNameContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#tupleOrArrayName.
    def exitTupleOrArrayName(self, ctx:ClickHouseParser.TupleOrArrayNameContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#keyword.
    def enterKeyword(self, ctx:ClickHouseParser.KeywordContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#keyword.
    def exitKeyword(self, ctx:ClickHouseParser.KeywordContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#keywordForAlias.
    def enterKeywordForAlias(self, ctx:ClickHouseParser.KeywordForAliasContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#keywordForAlias.
    def exitKeywordForAlias(self, ctx:ClickHouseParser.KeywordForAliasContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#alias.
    def enterAlias(self, ctx:ClickHouseParser.AliasContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#alias.
    def exitAlias(self, ctx:ClickHouseParser.AliasContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#identifier.
    def enterIdentifier(self, ctx:ClickHouseParser.IdentifierContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#identifier.
    def exitIdentifier(self, ctx:ClickHouseParser.IdentifierContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#identifierOrNull.
    def enterIdentifierOrNull(self, ctx:ClickHouseParser.IdentifierOrNullContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#identifierOrNull.
    def exitIdentifierOrNull(self, ctx:ClickHouseParser.IdentifierOrNullContext):
        pass


    # Enter a parse tree produced by ClickHouseParser#enumValue.
    def enterEnumValue(self, ctx:ClickHouseParser.EnumValueContext):
        pass

    # Exit a parse tree produced by ClickHouseParser#enumValue.
    def exitEnumValue(self, ctx:ClickHouseParser.EnumValueContext):
        pass



del ClickHouseParser