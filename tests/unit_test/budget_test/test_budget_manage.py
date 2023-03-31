import json
from http_service.api.v1.budget.http_api import http_set_budget_info_interface, http_get_budget_info_interface
from differential_privacy.accountant.budget import BudgetManager
from http_service.timer_task.budget_task import budget_recover
from tests.config.load_config import load_config


class Request:
    def __init__(self, json):
        self.json = json


budget_config = load_config("unit_test.ini", "budget")


def test_set_budget_info():
    key = {
        "prefix": budget_config.get("table_ip"),
        "db_name": "default",
        "table_name": "menu_page",
        "total_budget": 888888.0,
        "recover_cycle": 30,
        "exhausted_strategy": "reject",
    }
    request = Request(key)
    res = http_set_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 200


def test_set_budget_info_2():
    key = {
        "prefix": "1.1.1.1",
        "db_name": "test_db_22",
        "table_name": "test_table_222",
        "total_budget": 999.0,
        "recover_cycle": 15,
        "exhausted_strategy": "reject",
    }
    request = Request(key)
    res = http_set_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 200


def test_set_budget_info_3():
    key = {
        "prefix": "1.1.1.1",
        "db_name": "test_db",
        "table_name": "test_table",
        "total_budget": 999.0,
        "recover_cycle": 15,
        "exhausted_strategy": "reject",
    }
    request = Request(key)
    res = http_set_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 200


def test_set_budget_info_4():
    key = {
        "prefix": budget_config.get("table_ip"),
        "db_name": "default",
        "table_name": "menu",
        "total_budget": 888888.0,
        "recover_cycle": 30,
        "exhausted_strategy": "reject",
    }
    request = Request(key)
    res = http_set_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 200


def test_get_budget_info():
    key = {
        "prefix": "1.1.1.1",
        "db_name": "test_db",
        "table_name": "test_table",
    }
    request = Request(key)
    res = http_get_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 200


def test_get_budget_info_error():
    key = {
        "prefix": "1.1.1.1",
        "db_name": "error",
        "table_name": "test_table",
    }
    request = Request(key)
    res = http_get_budget_info_interface(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 1


def test_create_budget_table():
    budget_manager = BudgetManager()
    budget_manager.create_budget_table()


def test_budget_recover_task():
    budget_recover()


if __name__ == '__main__':
    # test_create_budget_table()
    test_set_budget_info()
    # test_set_budget_info_2()
    # test_set_budget_info_3()
    # test_set_budget_info_4()
    # test_get_budget_info()
    # test_get_budget_info_error()
    # test_budget_recover_task()
