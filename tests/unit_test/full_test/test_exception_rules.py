import json

from http_service.api.v1.query.http_query import dpsql_http_interface_query


class Request:
    def __init__(self, json):
        self.json = json


def test_reader_type_err():
    key = {
        "sql": "select * from menu_page limit 10",
        "dbconfig": {
            "reader": "ABase",
            "database": "rangers",
        },
        "queryconfig": {
            "traceid": "traceid",
        },
    }
    test = Request(key)
    res = dpsql_http_interface_query(test)
    res_json = json.loads(res)
    err_info = res_json.get("status").get("Message")
    standard = "(DbaccessError('reader type error', 'D3013'), 'Q5010')"
    assert err_info == standard
