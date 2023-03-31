import json
import logging
from tests.functional_test.corpus import clickhouse_single_test, clickhouse_join_test
from tests.functional_test.query.dpsql_query import query_sql_noise


def clickhouse_sample_query():
    sql_list = clickhouse_single_test
    for sql in sql_list:
        _test_sql(sql)


def _test_sql(q):
    print(q)
    res = query_sql_noise(q, "clickhouse")
    res_json = json.loads(res)
    status = res_json["status"]
    code = status["code"]
    if code == 1:
        logging.error("sql failed: %s, error message: %s" % (q, status["Message"]))
    print(res_json)


def clickhouse_join():
    sql_list = clickhouse_join_test
    for sql in sql_list:
        _test_sql(sql)


if __name__ == "__main__":
    clickhouse_sample_query()
    clickhouse_join()
