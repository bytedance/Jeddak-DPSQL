import json
from http_service.api.v1.query.http_query import dpsql_http_interface_query
from tests.unit_test.utils import DBCONFIG_FOR_CK


class Request:
    def __init__(self, json):
        self.json = json


def test_var():
    sql = "select VarPop(page_number) from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Laplace",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_std():
    sql = "select stddevPop(page_number) from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Laplace",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


if __name__ == '__main__':
    # test_var()
    test_std()
