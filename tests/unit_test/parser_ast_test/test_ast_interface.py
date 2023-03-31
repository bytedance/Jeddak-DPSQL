from parser.utils import ast_utils
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder
from parser.ast.type.node_type import NodeType, DialectType


def test_find_nodes():
    sql_expr1 = "sum(age) + count(name) + min(salary) + max(age) + avg(age) + varPop(age) + stddevPop(age)"
    expr1_ast = ast_utils.createExprNode(sql_expr1)
    nodes1 = ast_utils.findNodes(expr1_ast, NodeType.SqlAggFunction_EXPR)
    nodes1_2 = ast_utils.findNodes(expr1_ast, NodeType.SqlSumFunction_EXPR)
    nodes1_3 = ast_utils.findNodes(expr1_ast, NodeType.SqlCountFunction_EXPR)
    nodes1_4 = ast_utils.findNodes(expr1_ast, NodeType.SqlMinFunction_EXPR)
    nodes1_5 = ast_utils.findNodes(expr1_ast, NodeType.SqlMaxFunction_EXPR)
    nodes1_6 = ast_utils.findNodes(expr1_ast, NodeType.SqlAvgFunction_EXPR)
    nodes1_7 = ast_utils.findNodes(expr1_ast, NodeType.SqlVarPopFunction_EXPR)
    nodes1_8 = ast_utils.findNodes(expr1_ast, NodeType.SqlStdPopFunction_EXPR)
    assert len(nodes1) == 7
    assert len(nodes1_2) == 1
    assert len(nodes1_3) == 1
    assert len(nodes1_4) == 1
    assert len(nodes1_5) == 1
    assert len(nodes1_6) == 1
    assert len(nodes1_7) == 1
    assert len(nodes1_8) == 1

    sql_expr2 = "name = sunn and age == 10 and sex = male and not male or class = 3 or 10||11"
    sql_expr2_2 = "name is null and male is not null"
    sql_expr2_3 = "age1 >10 and age2 < 80 and age3 >= 20 and age4 <= 50"
    sql_expr2_4 = "UserID IN (123, 456) and UserID not IN (678, 901) and UserID global IN (123, 456) and country  global not in collection4"
    sql_expr2_5 = "CLUSTERS LIKE 'test%' and name not like 'su%' and age ILIKE '10' and sex not ILIKE 'ma'"
    expr2_ast = ast_utils.createExprNode(sql_expr2)
    expr2_2_ast = ast_utils.createExprNode(sql_expr2_2)
    expr2_3_ast = ast_utils.createExprNode(sql_expr2_3)
    expr2_4_ast = ast_utils.createExprNode(sql_expr2_4)
    expr2_5_ast = ast_utils.createExprNode(sql_expr2_5)
    nodes2 = ast_utils.findNodes(expr2_ast, NodeType.BinaryEqual_EXPR)
    nodes2_2 = ast_utils.findNodes(expr2_ast, NodeType.LogicalEqual_EXPR)
    nodes2_3 = ast_utils.findNodes(expr2_ast, NodeType.LogicalNot_EXPR)
    nodes2_4 = ast_utils.findNodes(expr2_ast, NodeType.LogicalAnd_EXPR)
    nodes2_5 = ast_utils.findNodes(expr2_ast, NodeType.LogicalOr_EXPR)
    nodes2_6 = ast_utils.findNodes(expr2_ast, NodeType.LogicalConcat_EXPR)
    nodes2_7 = ast_utils.findNodes(expr2_2_ast, NodeType.LogicalIsNull_EXPR)
    nodes2_8 = ast_utils.findNodes(expr2_3_ast, NodeType.LogicalCompare_EXPR)
    nodes2_9 = ast_utils.findNodes(expr2_4_ast, NodeType.LogicalIn_EXPR)
    nodes2_10 = ast_utils.findNodes(expr2_5_ast, NodeType.LogicalLike_EXPR)
    nodes2_11 = ast_utils.findNodes(expr2_ast, NodeType.BooleanCompare_EXPR)
    assert len(nodes2) == 3
    assert len(nodes2_2) == 1
    assert len(nodes2_3) == 1
    assert len(nodes2_4) == 3
    assert len(nodes2_5) == 2
    assert len(nodes2_6) == 1
    assert len(nodes2_7) == 2
    assert len(nodes2_8) == 4
    assert len(nodes2_9) == 4
    assert len(nodes2_10) == 4
    assert len(nodes2_11) == 11

    sql_expr3 = "if(age > 10, 20, 10 )"
    sql_expr3_2 = "case when event='purchase' then float_params{'slot_param_1'} else float_params{'curren_amount'} end"
    sql_expr3_3 = "multiIf(server_time < 1609948800, server_time, time > 2000000000, toUInt32(time / 1000), time)"
    sql_expr3_4 = "iif(age > 10, 20, 10 )"
    sql_expr3_5 = "age > 10 ? 20: 10"
    expr3_ast = ast_utils.createExprNode(sql_expr3)
    expr3_2_ast = ast_utils.createExprNode(sql_expr3_2)
    expr3_3_ast = ast_utils.createExprNode(sql_expr3_3)
    expr3_4_ast = ast_utils.createExprNode(sql_expr3_4)
    expr3_6_ast = ast_utils.createExprNode(sql_expr3_5)
    nodes3 = ast_utils.findNodes(expr3_ast, NodeType.IfExpression_EXPR)
    node3_2 = ast_utils.findNodes(expr3_2_ast, NodeType.CaseExpression_EXPR)
    node3_3 = ast_utils.findNodes(expr3_3_ast, NodeType.MultiIfExpression_EXPR)
    node3_4 = ast_utils.findNodes(expr3_4_ast, NodeType.IIFFunction_EXPR)
    node3_5 = ast_utils.findNodes(expr3_2_ast, NodeType.WhenExpression_EXPR)
    node3_6 = ast_utils.findNodes(expr3_6_ast, NodeType.TernaryExpression_EXPR)
    node3_7 = ast_utils.findNodes(expr3_ast, NodeType.CondExpression_EXPR)
    assert len(nodes3) == 1
    assert len(node3_2) == 1
    assert len(node3_3) == 1
    assert len(node3_4) == 1
    assert len(node3_5) == 1
    assert len(node3_6) == 1
    assert len(node3_7) == 1

    sql_expr4 = "myfunc(name) + abs(-10)"
    expr4_ast = ast_utils.createExprNode(sql_expr4)
    nodes4 = ast_utils.findNodes(expr4_ast, NodeType.CommonFunction_EXPR)
    node4_2 = ast_utils.findNodes(expr4_ast, NodeType.MathFunction_EXPR)
    node4_3 = ast_utils.findNodes(expr4_ast, NodeType.Function_EXPR)
    assert len(nodes4) == 1
    assert len(node4_2) == 1
    assert len(node4_3) == 2

    sql_expr5 = "select name from (select name1 as name from table1) cross join (select name2 as name from table2)"
    sql_expr5_2 = "select name from fusionMerge( rangers , tob_apps_all , tob_apps_realtime_all , event_date , multiIf ( server_time < 1609948800 , server_time , time > 2000000000 , toUInt32 ( time / 1000 ) , time ) , '[1633881600,1633881600]' , '(1633881600,1634486399]' ) et"
    builder = ClickHouseAstBuilder()
    expr5_ast = builder.get_query_ast(sql_expr5)
    expr5_ast_2 = builder.get_query_ast(sql_expr5_2)
    nodes5 = ast_utils.findNodes(expr5_ast, NodeType.SqlTableSource)
    nodes5_2 = ast_utils.findNodes(expr5_ast, NodeType.SqlTableJoinSource)
    nodes5_3 = ast_utils.findNodes(expr5_ast, NodeType.SqlSubquerySource)
    nodes5_4 = ast_utils.findNodes(expr5_ast, NodeType.SqlSource)
    nodes5_5 = ast_utils.findNodes(expr5_ast_2, NodeType.SqlFusionMergeSource)
    assert len(nodes5) == 2
    assert len(nodes5_2) == 1
    assert len(nodes5_3) == 2
    assert len(nodes5_4) == 5
    assert len(nodes5_5) == 1

    nodes6 = ast_utils.findNodes(expr5_ast, NodeType.Union_SQLSTATEMENT)
    assert len(nodes6) == 3


def test_convert_ast_to_sql():
    sql = "SELECT name FROM test_table"
    builder = ClickHouseAstBuilder()
    ast = builder.get_query_ast(sql)
    ast_str = ast_utils.tosql(ast, DialectType.CLICKHOUSE)
    ast_str_2 = ast_utils.tosql(ast, DialectType.HIVE)
    assert ast_str == sql
    assert ast_str_2 == sql


def test_judge_agg_node():
    sql_expr1 = "sum(age)"
    sql_expr2 = "summ(age)"
    sql_expr3 = "select sum(age)"
    expr1_ast = ast_utils.createExprNode(sql_expr1)
    expr2_ast = ast_utils.createExprNode(sql_expr2)
    expr3_ast = ClickHouseAstBuilder().get_query_ast(sql_expr3)
    assert ast_utils.isAggFunction("haha") is False
    assert ast_utils.isAggFunction(expr1_ast) is True
    assert ast_utils.isAggFunction(expr2_ast) is False
    assert ast_utils.isAggFunction(expr3_ast) is False


def test_replace_node():
    sql_expr1 = "sum(age) as sum_age"
    sql_expr2 = "count(age)"
    expr_ast = ast_utils.createExprNode(sql_expr1)
    expr_ast_2 = ast_utils.createExprNode(sql_expr2)
    ast_utils.replaceNode(expr_ast.expr, expr_ast_2)
    src1 = ast_utils.tosql(expr_ast, DialectType.CLICKHOUSE)
    assert src1 == "COUNT(age) AS sum_age"

    sql_expr3 = "(count(age)) as count_age"
    expr_ast_3 = ast_utils.createExprNode(sql_expr3)
    ast_utils.replaceNode(expr_ast_3.expr.expr, expr_ast_2)
    src2 = ast_utils.tosql(expr_ast_3, DialectType.CLICKHOUSE)
    assert src2 == "(COUNT(age)) AS count_age"

    sql_expr4 = "arrayMap(x -> addDays(start_date, x))"
    expr_ast_4 = ast_utils.createExprNode(sql_expr4)
    ast_utils.replaceNode(expr_ast_4.args[0].left_list[0], expr_ast_2)
    src3 = ast_utils.tosql(expr_ast_4, DialectType.CLICKHOUSE)
    assert src3 == "arrayMap((COUNT(age)) -> addDays(start_date, x))"

    expr_ast = ast_utils.createExprNode(sql_expr1)
    ast_utils.replaceNode(expr_ast.expr.args[0], expr_ast_2)
    src4 = ast_utils.tosql(expr_ast, DialectType.CLICKHOUSE)
    assert src4 == "SUM(COUNT(age)) AS sum_age"

    sql_expr5 = "-a + b"
    expr_ast_5 = ast_utils.createExprNode(sql_expr5)
    ast_utils.replaceNode(expr_ast_5.left.expr, expr_ast_2)
    src5 = ast_utils.tosql(expr_ast_5, DialectType.CLICKHOUSE)
    assert src5 == "-COUNT(age) + b"

    sql_expr6 = "if(age > 10, 20, 10 )"
    expr_ast_6 = ast_utils.createExprNode(sql_expr6)
    ast_utils.replaceNode(expr_ast_6.cond, expr_ast_2)
    src6 = ast_utils.tosql(expr_ast_6, DialectType.CLICKHOUSE)
    assert src6 == "if(COUNT(age),20,10)"
    ast_utils.replaceNode(expr_ast_6.then_expr, expr_ast_2)
    src6_2 = ast_utils.tosql(expr_ast_6, DialectType.CLICKHOUSE)
    assert src6_2 == "if(COUNT(age),COUNT(age),10)"
    ast_utils.replaceNode(expr_ast_6.else_expr, expr_ast_2)
    src6_3 = ast_utils.tosql(expr_ast_6, DialectType.CLICKHOUSE)
    assert src6_3 == "if(COUNT(age),COUNT(age),COUNT(age))"

    sql_expr7 = "multiIf(server_time < 1609948800, server_time, time > 2000000000, toUInt32(time / 1000), time)"
    expr_ast_7 = ast_utils.createExprNode(sql_expr7)
    ast_utils.replaceNode(expr_ast_7.args[1], expr_ast_2)
    src7 = ast_utils.tosql(expr_ast_7, DialectType.CLICKHOUSE)
    assert src7 == "multiIf(server_time < 1609948800 , COUNT(age) , time > 2000000000 , toUInt32(time/1000) , time)"

    sql_expr8 = "case when event='purchase' then float_params{'slot_param_1'} else float_params{'curren_amount'} end"
    expr_ast_8 = ast_utils.createExprNode(sql_expr8)
    ast_utils.replaceNode(expr_ast_8.case_expr, expr_ast_2)
    src8 = ast_utils.tosql(expr_ast_8, DialectType.CLICKHOUSE)
    assert src8 == "CASE  WHEN event = 'purchase' THEN float_params{'slot_param_1'} ELSE float_params{'curren_amount'} END"
    ast_utils.replaceNode(expr_ast_8.when_exprs[0], expr_ast_2)
    src8_2 = ast_utils.tosql(expr_ast_8, DialectType.CLICKHOUSE)
    assert src8_2 == "CASE  COUNT(age) ELSE float_params{'curren_amount'} END"
    ast_utils.replaceNode(expr_ast_8.else_expr, expr_ast_2)
    src8_3 = ast_utils.tosql(expr_ast_8, DialectType.CLICKHOUSE)
    assert src8_3 == "CASE  COUNT(age) ELSE COUNT(age) END"

    expr_ast_8 = ast_utils.createExprNode(sql_expr8)
    ast_utils.replaceNode(expr_ast_8.when_exprs[0].when_expr, expr_ast_2)
    src9 = ast_utils.tosql(expr_ast_8, DialectType.CLICKHOUSE)
    assert src9 == "CASE  WHEN COUNT(age) THEN float_params{'slot_param_1'} ELSE float_params{'curren_amount'} END"
    ast_utils.replaceNode(expr_ast_8.when_exprs[0].then_expr, expr_ast_2)
    src9_2 = ast_utils.tosql(expr_ast_8, DialectType.CLICKHOUSE)
    assert src9_2 == "CASE  WHEN COUNT(age) THEN COUNT(age) ELSE float_params{'curren_amount'} END"

    sql_expr10 = "age > 10 ? 20: 10"
    expr_ast_10 = ast_utils.createExprNode(sql_expr10)
    ast_utils.replaceNode(expr_ast_10.cond_expr, expr_ast_2)
    src10 = ast_utils.tosql(expr_ast_10, DialectType.CLICKHOUSE)
    assert src10 == "COUNT(age) ? 20 : 10"
    ast_utils.replaceNode(expr_ast_10.then_expr, expr_ast_2)
    src10_2 = ast_utils.tosql(expr_ast_10, DialectType.CLICKHOUSE)
    assert src10_2 == "COUNT(age) ? COUNT(age) : 10"
    ast_utils.replaceNode(expr_ast_10.else_expr, expr_ast_2)
    src10_3 = ast_utils.tosql(expr_ast_10, DialectType.CLICKHOUSE)
    assert src10_3 == "COUNT(age) ? COUNT(age) : COUNT(age)"

    sql_expr11 = "myfun(attr)(name)"
    expr_ast_11 = ast_utils.createExprNode(sql_expr11)
    ast_utils.replaceNode(expr_ast_11.column_list[0], expr_ast_2)
    src11 = ast_utils.tosql(expr_ast_11, DialectType.CLICKHOUSE)
    assert src11 == "myfun(COUNT(age))(name)"

    sql_expr12 = "not male"
    expr_ast_12 = ast_utils.createExprNode(sql_expr12)
    ast_utils.replaceNode(expr_ast_12.expr, expr_ast_2)
    src12 = ast_utils.tosql(expr_ast_12, DialectType.CLICKHOUSE)
    assert src12 == " NOT COUNT(age)"

    sql_expr13 = "sex = male"
    expr_ast_13 = ast_utils.createExprNode(sql_expr13)
    ast_utils.replaceNode(expr_ast_13.left, expr_ast_2)
    src13 = ast_utils.tosql(expr_ast_13, DialectType.CLICKHOUSE)
    assert src13 == "COUNT(age) = male"
    ast_utils.replaceNode(expr_ast_13.right, expr_ast_2)
    src13_2 = ast_utils.tosql(expr_ast_13, DialectType.CLICKHOUSE)
    assert src13_2 == "COUNT(age) = COUNT(age)"


def test_create_block_node():
    sql1 = "WITH '2019-08-01 15:23:00' as ts_upper_bound"
    ast_1 = ast_utils.createBlockNode(sql1, NodeType.With_BLOCKSTATEMENT)
    src1 = ast_utils.tosql(ast_1, DialectType.CLICKHOUSE)
    assert src1 == "WITH '2019-08-01 15:23:00' AS ts_upper_bound"
    assert ast_1.type == NodeType.With_BLOCKSTATEMENT

    sql2 = "select name, age"
    ast_2 = ast_utils.createBlockNode(sql2, NodeType.Select_BLOCKSTATEMENT)
    src2 = ast_utils.tosql(ast_2, DialectType.CLICKHOUSE)
    assert src2 == "SELECT name, age"
    assert ast_2.type == NodeType.Select_BLOCKSTATEMENT

    sql3 = "from table1 cross join table2"
    ast_3 = ast_utils.createBlockNode(sql3, NodeType.From_BLOCKSTATEMENT)
    src3 = ast_utils.tosql(ast_3, DialectType.CLICKHOUSE)
    assert src3 == "FROM table1  CROSS JOIN table2 "
    assert ast_3.type == NodeType.From_BLOCKSTATEMENT

    sql4 = "where age > 10"
    ast_4 = ast_utils.createBlockNode(sql4, NodeType.Where_BLOCKSTATEMENT)
    src4 = ast_utils.tosql(ast_4, DialectType.CLICKHOUSE)
    assert src4 == "WHERE age > 10"
    assert ast_4.type == NodeType.Where_BLOCKSTATEMENT

    sql5 = "group by class, sex"
    ast_5 = ast_utils.createBlockNode(sql5, NodeType.GroupBy_BLOCKSTATEMENT)
    src5 = ast_utils.tosql(ast_5, DialectType.CLICKHOUSE)
    assert src5 == " GROUP BY  (class , sex) "
    assert ast_5.type == NodeType.GroupBy_BLOCKSTATEMENT

    sql6 = "having age >20"
    ast_6 = ast_utils.createBlockNode(sql6, NodeType.Having_BLOCKSTATEMENT)
    src6 = ast_utils.tosql(ast_6, DialectType.CLICKHOUSE)
    assert src6 == "HAVING age > 20"
    assert ast_6.type == NodeType.Having_BLOCKSTATEMENT

    sql7 = "order by name, age"
    ast_7 = ast_utils.createBlockNode(sql7, NodeType.OrderBy_BLOCKSTATEMENT)
    src7 = ast_utils.tosql(ast_7, DialectType.CLICKHOUSE)
    assert src7 == "ORDER BY name   ,age   "
    assert ast_7.type == NodeType.OrderBy_BLOCKSTATEMENT

    sql8 = "limit 100"
    ast_8 = ast_utils.createBlockNode(sql8, NodeType.Limit_BLOCKSTATEMENT)
    src8 = ast_utils.tosql(ast_8, DialectType.CLICKHOUSE)
    assert src8 == "LIMIT 100 "
    assert ast_8.type == NodeType.Limit_BLOCKSTATEMENT

    sql9 = "LIMIT 5 BY domain, device_type"
    ast_9 = ast_utils.createBlockNode(sql9, NodeType.LimitBy_BLOCKSTATEMENT)
    src9 = ast_utils.tosql(ast_9, DialectType.CLICKHOUSE)
    assert src9 == "LIMIT 5 BY domain,device_type"
    assert ast_9.type == NodeType.LimitBy_BLOCKSTATEMENT

    sql10 = "TEALIMIT 1000 GROUP assumeNotNull(g0) ORDER cnt desc"
    ast_10 = ast_utils.createBlockNode(sql10, NodeType.TeaLimit_BLOCKSTATEMENT)
    src10 = ast_utils.tosql(ast_10, DialectType.CLICKHOUSE)
    assert src10 == "TEALIMIT 1000 GROUP assumeNotNull(g0) ORDER cnt DESC"
    assert ast_10.type == NodeType.TeaLimit_BLOCKSTATEMENT

    sql11 = "SETTINGS cpu = 4, memory = 16"
    ast_11 = ast_utils.createBlockNode(sql11, NodeType.Settings_BLOCKSTATEMENT)
    src11 = ast_utils.tosql(ast_11, DialectType.CLICKHOUSE)
    assert src11 == "SETTINGS cpu = 4,memory = 16"
    assert ast_11.type == NodeType.Settings_BLOCKSTATEMENT


if __name__ == "__main__":
    test_find_nodes()
    # test_convert_ast_to_sql()
    # test_judge_agg_node()
    # test_replace_node()
    # test_create_block_node()
