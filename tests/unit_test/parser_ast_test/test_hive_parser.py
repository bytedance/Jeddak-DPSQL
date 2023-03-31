import logging
from parser.utils import ast_utils
from parser.ast.builder.hive_query_ast_builder import HiveAstBuilder
from parser.ast.type.node_type import DialectType

query_list = [
    "select * from table1",
    "SELECT current_database()",
    "SELECT u.id, actions.date FROM ( SELECT av.uid AS uid  FROM action_video av WHERE av.date = '2008-06-03'  UNION ALL  SELECT ac.uid AS uid FROM action_comment ac WHERE ac.date = '2008-06-03') actions JOIN users u ON (u.id = actions.uid)",
    "select mymap['key1'], myarray[1] from tmp.sales_info_test  t1 where exists (select sku_name from tmp.sales_info_test2  t2 where  t1.sku_id = t2.sku_id)",
    "SELECT a.* FROM a JOIN b ON (a.id = b.id AND a.department = b.department)",
    "SELECT a.val, b.val, c.val FROM a JOIN b ON (a.key = b.key1) JOIN c ON (c.key = b.key2)",
    "SELECT a.val1, a.val2, b.val, c.val FROM a JOIN b ON (a.key = b.key) LEFT OUTER JOIN c ON (a.key = c.key)"
    "select binary('charels') from iteblog",
    "SELECT a.key, a.val FROM a LEFT SEMI JOIN b ON (a.key = b.key)",
    "select * from table1 where name = 'sunn'",
    # 'select * from table1 where name = "sunn"',
    "select nAme from mydatabase.table1",
    "select nvl(null,0)",
    "select 100",
    "select CAST(18446744073709001000 AS DECIMAL(38,0)) from my_table limit 1",
    "SELECT COALESCE(field_name,0) as value from table",
    "select NULLIF(e.job_id, j.job_id) from table",
    "select assert_true (2<1)",
    "SELECT col1, col2 FROM t1 CLUSTER BY col1",
    "SELECT col1, col2 from table1 SORT BY col1, col2",
    "SELECT col1, col2 FROM t1 DISTRIBUTE BY col1 SORT BY col1 ASC, col2 DESC",
    "SELECT col1, col2 FROM t1 CLUSTER BY col1",

]


def _test_sql_list(sql_list):
    errno = 0
    for item in sql_list:
        try:
            builder = HiveAstBuilder()
            ast = builder.get_query_ast(item)
            logging.info("ast : " + ast_utils.tosql(ast, DialectType.HIVE))
        except Exception as err:
            errno = errno + 1
            logging.error("error : %s" % str(err))
    assert errno == 0


def test_hive_parser():
    _test_sql_list(query_list)
