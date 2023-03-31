import json
import logging
from tests.functional_test.corpus import hive_single_test
from tests.functional_test.query.dpsql_query import query_sql_noise


def hive_sample_query():
    sql_list = hive_single_test
    for sql in sql_list:
        _test_sql(sql)


def _test_sql(q):
    print(q)
    res = query_sql_noise(q, "hivereader")
    print(res)
    res_json = json.loads(res)
    status = res_json["status"]
    code = status["code"]
    if code == 1:
        logging.error("sql failed: %s, error message: %s" % (q, status["Message"]))
    print(res_json)


if __name__ == "__main__":
    hive_sample_query()
