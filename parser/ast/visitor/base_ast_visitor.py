from parser.ast.visitor.tree_visitor import TreeVisitor


class BaseAstVisitor(TreeVisitor):

    # begin visit query statement ====================================
    def preVisitUnionSelectStatement(self, node):
        pass

    def visitUnionSelectStatement(self, query_node):
        pass

    def postVisitUnionSelectStatement(self, node):
        pass

    def preVisitSelectStatement(self, node):
        pass

    def visitSelectStatement(self, query_node):
        pass

    def postVisitSelectStatement(self, node):
        pass

    def preVisitClickHouseSelectStatement(self, node):
        pass

    def visitClickHouseSelectStatement(self, query_node):
        pass

    def postVisitClickHouseSelectStatement(self, node):
        pass

    def preVisitByteClickHouseSelectStatement(self, node):
        pass

    def visitByteClickHouseSelectStatement(self, query_node):
        pass

    def postVisitByteClickHouseSelectStatement(self, node):
        pass

    def preVisitHiveSelectStatement(self, node):
        pass

    def visitHiveSelectStatement(self, node):
        pass

    def postVisitHiveSelectStatement(self, node):
        pass

    def preVisitSelectBlockStatement(self, node):
        pass

    def visitSelectBlockStatement(self, node):
        pass

    def postVisitSelectBlockStatement(self, node):
        pass

    def preVisitFromBlockStatement(self, node):
        pass

    def visitFromBlockStatement(self, node):
        pass

    def postVisitFromBlockStatement(self, node):
        pass

    def preVisitArrayJoinBlockStatement(self, node):
        pass

    def visitArrayJoinBlockStatement(self, node):
        pass

    def postVisitArrayJoinBlockStatement(self, node):
        pass

    def preVisitWhereBlockStatement(self, node):
        pass

    def visitWhereBlockStatement(self, node):
        pass

    def postVisitWhereBlockStatement(self, node):
        pass

    def preVisitGroupByBlockStatement(self, node):
        pass

    def visitGroupByBlockStatement(self, node):
        pass

    def postVisitGroupByBlockStatement(self, node):
        pass

    def preVisitHavingBlockStatement(self, node):
        pass

    def visitHavingBlockStatement(self, node):
        pass

    def postVisitHavingBlockStatement(self, node):
        pass

    def preVisitOrderByBlockStatement(self, node):
        pass

    def visitOrderByBlockStatement(self, node):
        pass

    def postVisitOrderByBlockStatement(self, node):
        pass

    def preVisitLimitByBlockStatement(self, node):
        pass

    def visitLimitByBlockStatement(self, node):
        pass

    def postVisitLimitByBlockStatement(self, node):
        pass

    def preVisitLimitBlockStatement(self, node):
        pass

    def visitLimitBlockStatement(self, node):
        pass

    def postVisitLimitBlockStatement(self, node):
        pass

    def preVisitTeaLimitBlockStatement(self, node):
        pass

    def visitTeaLimitBlockStatement(self, node):
        pass

    def postVisitTeaLimitBlockStatement(self, node):
        pass

    def preVisitSettingsBlockStatement(self, node):
        pass

    def visitSettingsBlockStatement(self, node):
        pass

    def postVisitSettingsBlockStatement(self, node):
        pass

    def preVisitWithBlockStatement(self, node):
        pass

    def visitWithBlockStatement(self, node):
        pass

    def postVisitWithBlockStatement(self, node):
        pass

    def preVisitPrewhereBlockStatement(self, node):
        pass

    def visitPrewhereBlockStatement(self, node):
        pass

    def postVisitPrewhereBlockStatement(self, node):
        pass

    def preVisitSampleBlockStatement(self, node):
        pass

    def visitSampleBlockStatement(self, node):
        pass

    def postVisitSampleBlockStatement(self, node):
        pass

    def preVisitClusterByBlockStatement(self, node):
        pass

    def visitClusterByBlockStatement(self, node):
        pass

    def postVisitClusterByBlockStatement(self, node):
        pass

    def preVisitDistributeByBlockStatement(self, node):
        pass

    def visitDistributeByBlockStatement(self, node):
        pass

    def postVisitDistributeByBlockStatement(self, node):
        pass

    def preVisitSortByBlockStatement(self, node):
        pass

    def visitSortByBlockStatement(self, node):
        pass

    def postVisitSortByBlockStatement(self, node):
        pass

    # begin visit base expr ====================================
    def preVisitLiteral(self, node):
        pass

    def visitLiteral(self, node):
        pass

    def postVisitLiteral(self, node):
        pass

    def preVisitIdentifier(self, node):
        pass

    def visitIdentifier(self, node):
        pass

    def postVisitIdentifier(self, node):
        pass

    def preVisitNumber(self, node):
        pass

    def visitNumber(self, node):
        pass

    def postVisitNumber(self, node):
        pass

    def preVisitColumn(self, node):
        pass

    def visitColumn(self, node):
        pass

    def postVisitColumn(self, node):
        pass

    def preVisitAllColumns(self, node):
        pass

    def visitAllColumns(self, node):
        pass

    def postVisitAllColumns(self, node):
        pass

    def preVisitArrayAccess(self, node):
        pass

    def visitArrayAccess(self, node):
        pass

    def postVisitArrayAccess(self, node):
        pass

    def preVisitTupleAccess(self, node):
        pass

    def visitTupleAccess(self, node):
        pass

    def postVisitTupleAccess(self, node):
        pass

    def preVisitArrays(self, node):
        pass

    def visitArrays(self, node):
        pass

    def postVisitArrays(self, node):
        pass

    def preVisitTuples(self, node):
        pass

    def visitTuples(self, node):
        pass

    def postVisitTuples(self, node):
        pass

    def preVisitMapExpression(self, node):
        pass

    def visitMapExpression(self, node):
        pass

    def postVisitMapExpression(self, node):
        pass

    def preVisitTable(self, node):
        pass

    def visitTable(self, node):
        pass

    def postVisitTable(self, node):
        pass

    def preVisitTableFunctionExpr(self, node):
        pass

    def visitTableFunctionExpr(self, node):
        pass

    def postVisitTableFunctionExpr(self, node):
        pass

    def preVisitMaps(self, node):
        pass

    def visitMaps(self, node):
        pass

    def postVisitMaps(self, node):
        pass

    # begin visit complex expr ====================================
    def preVisitNameExpression(self, node):
        pass

    def visitNameExpression(self, node):
        pass

    def postVisitNameExpression(self, node):
        pass

    def preVisitNestedExpression(self, node):
        pass

    def visitNestedExpression(self, node):
        pass

    def postVisitNestedExpression(self, node):
        pass

    def preVisitInterval(self, node):
        pass

    def visitInterval(self, node):
        pass

    def postVisitInterval(self, node):
        pass

    def preVisitLambdaExpression(self, node):
        pass

    def visitLambdaExpression(self, node):
        pass

    def postVisitLambdaExpression(self, node):
        pass

    def preVisitCastExpr(self, node):
        pass

    def visitCastExpr(self, node):
        pass

    def postVisitCastExpr(self, node):
        pass

    def preVisitRatioExpr(self, node):
        pass

    def visitRatioExpr(self, node):
        pass

    def postVisitRatioExpr(self, node):
        pass

    def preVisitTopExpr(self, node):
        pass

    def visitTopExpr(self, node):
        pass

    def postVisitTopExpr(self, node):
        pass

    def preVisitLimitExpr(self, node):
        pass

    def visitLimitExpr(self, node):
        pass

    def postVisitLimitExpr(self, node):
        pass

    def preVisitJoinConstraintExpr(self, node):
        pass

    def visitJoinConstraintExpr(self, node):
        pass

    def postVisitJoinConstraintExpr(self, node):
        pass

    def preVisitOrderExpr(self, node):
        pass

    def visitOrderExpr(self, node):
        pass

    def postVisitOrderExpr(self, node):
        pass

    def preVisitEnumExpr(self, node):
        pass

    def visitEnumExpr(self, node):
        pass

    def postVisitEnumExpr(self, node):
        pass

    def preVisitDateExpr(self, node):
        pass

    def visitDateExpr(self, node):
        pass

    def postVisitDateExpr(self, node):
        pass

    def preVisitTokenDefinitionExpr(self, node):
        pass

    def visitTokenDefinitionExpr(self, node):
        pass

    def postVisitTokenDefinitionExpr(self, node):
        pass

    def preVisitSelectItem(self, node):
        pass

    def visitSelectItem(self, node):
        pass

    def postVisitSelectItem(self, node):
        pass

    def preVisitSampleExpr(self, node):
        pass

    def visitSampleExpr(self, node):
        pass

    def postVisitSampleExpr(self, node):
        pass

    def preVisitValueTypeDefinitionExpr(self, node):
        pass

    def visitValueTypeDefinitionExpr(self, node):
        pass

    def postVisitValueTypeDefinitionExpr(self, node):
        pass

    def preVisitFormatExpr(self, node):
        pass

    def visitFormatExpr(self, node):
        pass

    def postVisitFormatExpr(self, node):
        pass

    def preVisitBinaryExpr(self, node):
        pass

    def visitBinaryExpr(self, node):
        pass

    def postVisitBinaryExpr(self, node):
        pass

    # begin visit agg function ====================================
    def preVisitSqlAggFunction(self, node):
        pass

    def visitSqlAggFunction(self, node):
        pass

    def postVisitSqlAggFunction(self, node):
        pass

    def preVisitSqlCountFunction(self, node):
        pass

    def visitSqlCountFunction(self, node):
        pass

    def postVisitSqlCountFunction(self, node):
        pass

    def preVisitSqlMinFunction(self, node):
        pass

    def visitSqlMinFunction(self, node):
        pass

    def postVisitSqlMinFunction(self, node):
        pass

    def preVisitSqlMaxFunction(self, node):
        pass

    def visitSqlMaxFunction(self, node):
        pass

    def postVisitSqlMaxFunction(self, node):
        pass

    def preVisitSqlSumFunction(self, node):
        pass

    def visitSqlSumFunction(self, node):
        pass

    def postVisitSqlSumFunction(self, node):
        pass

    def preVisitSqlAvgFunction(self, node):
        pass

    def visitSqlAvgFunction(self, node):
        pass

    def postVisitSqlAvgFunction(self, node):
        pass

    def preVisitSqlVarPopFunction(self, node):
        pass

    def visitSqlVarPopFunction(self, node):
        pass

    def postVisitSqlVarPopFunction(self, node):
        pass

    def preVisitSqlVarSampFunction(self, node):
        pass

    def visitSqlVarSampFunction(self, node):
        pass

    def postVisitSqlVarSampFunction(self, node):
        pass

    def preVisitSqlStdPopFunction(self, node):
        pass

    def visitSqlStdPopFunction(self, node):
        pass

    def postVisitSqlStdPopFunction(self, node):
        pass

    def preVisitSqlStdSampFunction(self, node):
        pass

    def visitSqlStdSampFunction(self, node):
        pass

    def postVisitSqlStdSampFunction(self, node):
        pass

    # begin visit arithmetic ====================================
    def preVisitNegateExpression(self, node):
        pass

    def visitNegateExpression(self, node):
        pass

    def postVisitNegateExpression(self, node):
        pass

    def preVisitMultiplyExpression(self, node):
        pass

    def visitMultiplyExpression(self, node):
        pass

    def postVisitMultiplyExpression(self, node):
        pass

    def preVisitDivideExpression(self, node):
        pass

    def visitDivideExpression(self, node):
        pass

    def postVisitDivideExpression(self, node):
        pass

    def preVisitModuloExpression(self, node):
        pass

    def visitModuloExpression(self, node):
        pass

    def postVisitModuloExpression(self, node):
        pass

    def preVisitAdditionExpression(self, node):
        pass

    def visitAdditionExpression(self, node):
        pass

    def postVisitAdditionExpression(self, node):
        pass

    def preVisitSubtractionExpression(self, node):
        pass

    def visitSubtractionExpression(self, node):
        pass

    def postVisitSubtractionExpression(self, node):
        pass

    def preVisitDivExpression(self, node):
        pass

    def visitDivExpression(self, node):
        pass

    def postVisitDivExpression(self, node):
        pass

    # begin visit cond expression ====================================
    def preVisitIfExpression(self, node):
        pass

    def visitIfExpression(self, node):
        pass

    def postVisitIfExpression(self, node):
        pass

    def preVisitIIFFunction(self, node):
        pass

    def visitIIFFunction(self, node):
        pass

    def postVisitIIFFunction(self, node):
        pass

    def preVisitMultiIfExpression(self, node):
        pass

    def visitMultiIfExpression(self, node):
        pass

    def postVisitMultiIfExpression(self, node):
        pass

    def preVisitCaseExpression(self, node):
        pass

    def visitCaseExpression(self, node):
        pass

    def postVisitCaseExpression(self, node):
        pass

    def preVisitWhenExpression(self, node):
        pass

    def visitWhenExpression(self, node):
        pass

    def postVisitWhenExpression(self, node):
        pass

    def preVisitTernaryExpression(self, node):
        pass

    def visitTernaryExpression(self, node):
        pass

    def postVisitTernaryExpression(self, node):
        pass

    def preVisitNvlFuncExpressio(self, node):
        pass

    def visitNvlFuncExpressio(self, node):
        pass

    def postVisitNvlFuncExpressio(self, node):
        pass

    def preVisitCoalesceFuncExpression(self, node):
        pass

    def visitCoalesceFuncExpression(self, node):
        pass

    def postVisitCoalesceFuncExpression(self, node):
        pass

    def preVisitNullIfFuncExpression(self, node):
        pass

    def visitNullIfFuncExpression(self, node):
        pass

    def postVisitNullIfFuncExpression(self, node):
        pass

    def preVisitAssertTrueFuncExpression(self, node):
        pass

    def visitAssertTrueFuncExpression(self, node):
        pass

    def postVisitAssertTrueFuncExpression(self, node):
        pass

    # begin visit function ====================================
    def preVisitCommonFunction(self, node):
        pass

    def visitCommonFunction(self, node):
        pass

    def postVisitCommonFunction(self, node):
        pass

    def preVisitExtractFunction(self, node):
        pass

    def visitExtractFunction(self, node):
        pass

    def postVisitExtractFunction(self, node):
        pass

    def preVisitMathFunction(self, node):
        pass

    def visitMathFunction(self, node):
        pass

    def postVisitMathFunction(self, node):
        pass

    def preVisitBareFunction(self, node):
        pass

    def visitBareFunction(self, node):
        pass

    def postVisitBareFunction(self, node):
        pass

    def preVisitRoundFunction(self, node):
        pass

    def visitRoundFunction(self, node):
        pass

    def postVisitRoundFunction(self, node):
        pass

    def preVisitPowerFunction(self, node):
        pass

    def visitPowerFunction(self, node):
        pass

    def postVisitPowerFunction(self, node):
        pass

    def preVisitQuantilesFunction(self, node):
        pass

    def visitQuantilesFunction(self, node):
        pass

    def postVisitQuantilesFunction(self, node):
        pass

    def preVisitQuantiles2Function(self, node):
        pass

    def visitQuantiles2Function(self, node):
        pass

    def postVisitQuantiles2Function(self, node):
        pass

    def preVisitQuantiles3Function(self, node):
        pass

    def visitQuantiles3Function(self, node):
        pass

    def postVisitQuantiles3Function(self, node):
        pass

    def preVisitClickHouseCommonFunction(self, node):
        pass

    def visitClickHouseCommonFunction(self, node):
        pass

    def postVisitClickHouseCommonFunction(self, node):
        pass

    def preVisitTrimFunction(self, node):
        pass

    def visitTrimFunction(self, node):
        pass

    def postVisitTrimFunction(self, node):
        pass

    def preVisitColumnsFunction(self, node):
        pass

    def visitColumnsFunction(self, node):
        pass

    def postVisitColumnsFunction(self, node):
        pass

    def preVisitToTypeNameFunction(self, node):
        pass

    def visitToTypeNameFunction(self, node):
        pass

    def postVisitToTypeNameFunction(self, node):
        pass

    # begin visit logical bool ====================================
    def preVisitBinaryEqual(self, node):
        pass

    def visitBinaryEqual(self, node):
        pass

    def postVisitBinaryEqual(self, node):
        pass

    def preVisitLogicalEqual(self, node):
        pass

    def visitLogicalEqual(self, node):
        pass

    def postVisitLogicalEqual(self, node):
        pass

    def preVisitLogicalNot(self, node):
        pass

    def visitLogicalNot(self, node):
        pass

    def postVisitLogicalNot(self, node):
        pass

    def preVisitLogicalAnd(self, node):
        pass

    def visitLogicalAnd(self, node):
        pass

    def postVisitLogicalAnd(self, node):
        pass

    def preVisitLogicalOr(self, node):
        pass

    def visitLogicalOr(self, node):
        pass

    def postVisitLogicalOr(self, node):
        pass

    def preVisitLogicalConcat(self, node):
        pass

    def visitLogicalConcat(self, node):
        pass

    def postVisitLogicalConcat(self, node):
        pass

    def preVisitLogicalIsNull(self, node):
        pass

    def visitLogicalIsNull(self, node):
        pass

    def postVisitLogicalIsNull(self, node):
        pass

    def preVisitLogicalCompare(self, node):
        pass

    def visitLogicalCompare(self, node):
        pass

    def postVisitLogicalCompare(self, node):
        pass

    def preVisitLogicalIn(self, node):
        pass

    def visitLogicalIn(self, node):
        pass

    def postVisitLogicalIn(self, node):
        pass

    def preVisitLogicalLike(self, node):
        pass

    def visitLogicalLike(self, node):
        pass

    def postVisitLogicalLike(self, node):
        pass

    def preVisitLogicalBetween(self, node):
        pass

    def visitLogicalBetween(self, node):
        pass

    def postVisitLogicalBetween(self, node):
        pass

    def preVisitLogicalIsTrue(self, node):
        pass

    def visitLogicalIsTrue(self, node):
        pass

    def postVisitLogicalIsTrue(self, node):
        pass

    def preVisitExistsQuery(self, node):
        pass

    def visitExistsQuery(self, node):
        pass

    def postVisitExistsQuery(self, node):
        pass

    # begin visit table source ====================================
    def preVisitSqlTableSource(self, node):
        pass

    def visitSqlTableSource(self, node):
        pass

    def postVisitSqlTableSource(self, node):
        pass

    def preVisitSqlTableJoinSource(self, node):
        pass

    def visitSqlTableJoinSource(self, node):
        pass

    def postVisitSqlTableJoinSource(self, node):
        pass

    def preVisitSqlUnionSource(self, node):
        pass

    def visitSqlUnionSource(self, node):
        pass

    def postVisitSqlUnionSource(self, node):
        pass

    def preVisitSqlSubquerySource(self, node):
        pass

    def visitSqlSubquerySource(self, node):
        pass

    def postVisitSqlSubquerySource(self, node):
        pass

    def preVisitSqlArrayJoinSource(self, node):
        pass

    def visitSqlArrayJoinSource(self, node):
        pass

    def postVisitSqlArrayJoinSource(self, node):
        pass

    def preVisitFusionMergeSource(self, node):
        pass

    def visitFusionMergeSource(self, node):
        pass

    def postVisitFusionMergeSource(self, node):
        pass
