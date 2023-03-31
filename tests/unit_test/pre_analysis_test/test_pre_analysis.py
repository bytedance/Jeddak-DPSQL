from analysis.syntax_feature import SqlAllFeature, AggOuterOperationFeature, AggScopeFeature, AggInnerParamFeature
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder
from analysis.pre_analysis_center import PreAnalysisCenter, NoiseSwitch


def test_getBasicMetaInfo():
    sql = "SELECT transform(ifNull(age, 'null'),[''],['unknown']) as g0 , count(distinct hash_uid) as cnt       FROM rangers.tob_apps_all et SAMPLE 1/100        WHERE tea_app_id = 7744 and (event_date >= '2021-10-25' and event_date <= '2021-10-31' and multiIf(server_time < 1609948800, server_time, time > 2000000000, toUInt32(time / 1000), time) >= 1635091200 and multiIf(server_time < 1609948800, server_time, time > 2000000000, toUInt32(time / 1000), time) <= 1635695999) and ((( (ifNull(device_id,'null') not in ('null','','-1','0')) AND ifNull(os_name,'null') in('ios','android') )))  group by g0        ORDER BY cnt DESC       LIMIT 1000"
    builder = ClickHouseAstBuilder()
    ast = builder.get_query_ast(sql)

    pac = PreAnalysisCenter()
    meta_info = pac.getBasicMetaInfo(ast)
    assert (meta_info.database == "rangers")
    assert (meta_info.table[0] == "tob_apps_all")
    assert (meta_info.tea_app_id == "7744")


def test_getStructInfo():
    sql1 = "with 5 as q1, x as (select number+100 as b, number as a from numbers(10) where number > q1) select * from x"
    builder = ClickHouseAstBuilder()
    ast = builder.get_query_ast(sql1)

    pac = PreAnalysisCenter()
    sturct_info = pac.getStructInfo(ast)
    assert SqlAllFeature.WITH_BLOCK in sturct_info.struct_feature_info

    sql2 = "SELECT _1700014057908, _1700014059578, _sum_1700014057914, _sum_1700014057915 FROM (SELECT (sum(report_cnt)) AS _sum_1700014057914, (p_date) AS _1700014057908, (sum(re_report_ucnt)) AS _sum_1700014057915 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01')  AND (p_date <= '2022-02-14')) AND ((app_id) = (1870))  AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, _68c4cc32b4 / _376152a9f3 AS _1700014059578 FROM (SELECT (sum(re_report_ucnt)) AS _68c4cc32b4, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, sum(_e10449b93d) AS _376152a9f3 FROM (SELECT _1700014057908, _d1da3897f8 FROM (SELECT (((app_id), (p_date))) AS _d1da3897f8, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod` WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908, _d1da3897f8) GROUP BY _1700014057908, _d1da3897f8) LEFT OUTER JOIN (SELECT (((app_id), (p_date))) AS _d1da3897f8, (avg((dau))) AS _e10449b93d FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE ((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')))) GROUP BY _d1da3897f8) USING (_d1da3897f8) GROUP BY _1700014057908) USING (_1700014057908)) USING (_1700014057908) ORDER BY _1700014057908 ASC LIMIT 10000 SETTINGS max_memory_usage=21474836480"
    ast2 = builder.get_query_ast(sql2)
    sturct_info2 = pac.getStructInfo(ast2)
    assert SqlAllFeature.JOIN_OPERATOR_CONTAIN_SUBQUERY in sturct_info2.struct_feature_info
    assert SqlAllFeature.JOIN_NESTED_JOIN in sturct_info2.struct_feature_info

    sql3 = "SELECT myfunc(count(id)), name FROM table1 cross join table2"
    ast3 = builder.get_query_ast(sql3)
    sturct_info3 = pac.getStructInfo(ast3)
    assert SqlAllFeature.JOIN_OPERATOR_ALL_TABLE in sturct_info3.struct_feature_info


def test_getAggInfo():
    sql1 = "SELECT myfunc(count(id)), name FROM test_table"
    builder = ClickHouseAstBuilder()
    ast1 = builder.get_query_ast(sql1)

    pac = PreAnalysisCenter()
    agg_info1 = pac.getAggInfo(ast1)
    assert len(agg_info1.agg_info_list) == 1
    assert AggOuterOperationFeature.FUNC_ALL in agg_info1.agg_info_list[0].agg_feature_info
    assert agg_info1.agg_info_list[0].scope_info == AggScopeFeature.SCOPE_OUTER

    sql2 = "SELECT _1700014057908, _1700014059578, _sum_1700014057914, _sum_1700014057915 FROM (SELECT (sum(report_cnt)) AS _sum_1700014057914, (p_date) AS _1700014057908, (sum(re_report_ucnt)) AS _sum_1700014057915 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01')  AND (p_date <= '2022-02-14')) AND ((app_id) = (1870))  AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, _68c4cc32b4 / _376152a9f3 AS _1700014059578 FROM (SELECT (sum(re_report_ucnt)) AS _68c4cc32b4, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, sum(_e10449b93d) AS _376152a9f3 FROM (SELECT _1700014057908, _d1da3897f8 FROM (SELECT (((app_id), (p_date))) AS _d1da3897f8, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod` WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908, _d1da3897f8) GROUP BY _1700014057908, _d1da3897f8) LEFT OUTER JOIN (SELECT (((app_id), (p_date))) AS _d1da3897f8, (avg((dau))) AS _e10449b93d FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE ((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')))) GROUP BY _d1da3897f8) USING (_d1da3897f8) GROUP BY _1700014057908) USING (_1700014057908)) USING (_1700014057908) ORDER BY _1700014057908 ASC LIMIT 10000 SETTINGS max_memory_usage=21474836480"
    ast2 = builder.get_query_ast(sql2)
    agg_info2 = pac.getAggInfo(ast2)
    assert len(agg_info2.agg_info_list) == 5
    assert agg_info2.agg_ref_feature_info == AggInnerParamFeature.AGG_REF
    assert agg_info2.outer_agg_position_info == AggScopeFeature.SCOPE_NO_OUTER


def test_getNoiseSwitchInfo():
    sql1 = "SELECT myfunc(count(id)), name FROM test_table"

    builder = ClickHouseAstBuilder()
    ast1 = builder.get_query_ast(sql1)

    pac = PreAnalysisCenter()
    noise_switch_info1 = pac.getNoiseSwitch(ast1)
    assert noise_switch_info1 == NoiseSwitch.NOT_NOISE

    sql2 = "SELECT count(id), name FROM test_table"
    ast2 = builder.get_query_ast(sql2)
    noise_switch_info2 = pac.getNoiseSwitch(ast2)
    assert noise_switch_info2 == NoiseSwitch.NOISE_POST_PROCESS

    sql3 = "SELECT count_id, name FROM (select count(id) as count_id,  name from test_table)"
    ast3 = builder.get_query_ast(sql3)
    noise_switch_info3 = pac.getNoiseSwitch(ast3)
    assert noise_switch_info3 == NoiseSwitch.NOISE_REWRITE_PROCESS

    sql4 = "SELECT _1700014057908, _1700014059578, _sum_1700014057914, _sum_1700014057915 FROM (SELECT (sum(report_cnt)) AS _sum_1700014057914, (p_date) AS _1700014057908, (sum(re_report_ucnt)) AS _sum_1700014057915 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01')  AND (p_date <= '2022-02-14')) AND ((app_id) = (1870))  AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, _68c4cc32b4 / _376152a9f3 AS _1700014059578 FROM (SELECT (sum(re_report_ucnt)) AS _68c4cc32b4, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908) LEFT OUTER JOIN (SELECT _1700014057908, sum(_e10449b93d) AS _376152a9f3 FROM (SELECT _1700014057908, _d1da3897f8 FROM (SELECT (((app_id), (p_date))) AS _d1da3897f8, (p_date) AS _1700014057908 FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod` WHERE (((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')) AND ((app_id) = (1870)) AND ((report_source) = ('ALL')) AND ((report_type) = ('ALL')) AND ((sec_type) = ('ALL'))))) GROUP BY _1700014057908, _d1da3897f8) GROUP BY _1700014057908, _d1da3897f8) LEFT OUTER JOIN (SELECT (((app_id), (p_date))) AS _d1da3897f8, (avg((dau))) AS _e10449b93d FROM `aeolus_data_db_aeolus_iota_202202`.`aeolus_data_table_8_573109_prod`  WHERE ((((p_date >= '2022-02-01') AND (p_date <= '2022-02-14')))) GROUP BY _d1da3897f8) USING (_d1da3897f8) GROUP BY _1700014057908) USING (_1700014057908)) USING (_1700014057908) ORDER BY _1700014057908 ASC LIMIT 10000 SETTINGS max_memory_usage=21474836480"
    ast4 = builder.get_query_ast(sql4)
    noise_switch_info4 = pac.getNoiseSwitch(ast4)
    assert noise_switch_info4 == NoiseSwitch.NOT_NOISE

    sql5 = "select value from (select count(id) + count(id) as value from menu inner join menu_page on menu.id = menu_page.menu_id)"
    ast5 = builder.get_query_ast(sql5)
    noise_switch_info4 = pac.getNoiseSwitch(ast5)
    assert noise_switch_info4 == NoiseSwitch.NOISE_REWRITE_PROCESS
