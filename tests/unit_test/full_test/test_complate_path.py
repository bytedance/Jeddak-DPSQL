"""
FullLinkTest
"""
from tests.unit_test.utils import DPSQL_TEST, QUERTCONFIG, CLICKHOUSE_READER, DBCONFIG_FOR_CK, HIVE_DB_CONFIG, \
    HIVE_READER
import logging

sql_list = ["select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"]
sql_num = 0


def test_clickhouse_sql():
    for sql in sql_list:
        _test_sql(sql)


def _test_sql(q):
    try:
        logging.error("-" * 50)
        global sql_num
        logging.error(str(sql_num) + " sql test:" + q)
        sql_num += 1
        res = CLICKHOUSE_READER.execute(q, DBCONFIG_FOR_CK, QUERTCONFIG)
        logging.error("original result:\n" + str(res))
        DPSQL_TEST.context.set_context("extra", None)
        dpres = DPSQL_TEST.execute(sql=q, dbconfig=DBCONFIG_FOR_CK, queryconfig=QUERTCONFIG)
        dpres = dpres.get_query_result()
        logging.error("DPSQL result:\n" + str(dpres))
        cmp = res.compare(dpres, 0.8)
        if cmp is False:
            logging.error("sql failed: %s " % (q,))
        else:
            logging.error("sql successed: %s " % (q,))
        return cmp
    except Exception as err:
        logging.exception(str(err))
        logging.error("sql failed: %s " % (q,))
        return False


def test_hive_sql():
    q = "select gender, sum(age) as total_age from user_info group by gender"
    try:
        logging.error(str(sql_num) + " sql test:" + q)
        res = HIVE_READER.execute(q, HIVE_DB_CONFIG, QUERTCONFIG)
        logging.error("original result:\n" + str(res))
        DPSQL_TEST.context.set_context("extra", None)
        dpres = DPSQL_TEST.execute(sql=q, dbconfig=HIVE_DB_CONFIG, queryconfig=QUERTCONFIG)
        dpres = dpres.get_query_result()
        logging.error("DPSQL result:\n" + str(dpres))
        cmp = res.compare(dpres, 0.8)
        if cmp is False:
            logging.error("sql failed: %s " % (q,))
        else:
            logging.error("sql successed: %s " % (q,))
        return cmp
    except Exception as err:
        logging.exception(str(err))
        logging.error("sql failed: %s " % (q,))
        return False


if __name__ == "__main__":
    test_clickhouse_sql()
