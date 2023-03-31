import json
from http_service.api.v1.query.http_query import dpsql_http_interface_query
from tests.unit_test.utils import DBCONFIG_FOR_CK
from differential_privacy.accountant.init_config import init_dpconfig
from query_driver.dpsql import DPSQL


class Request:
    def __init__(self, json):
        self.json = json


def test_init_dpconfig_null():
    dpconfig = init_dpconfig()
    target_dpconfig = {
        "dp_method": "Laplace",
        "budget_setting": {
            "epsilon": 0.9,
            "delt": 0,
        }
    }
    assert dpconfig == target_dpconfig


def test_init_dpconfig_gauss():
    source_dpconfig = {
        "dp_method": "Gauss",
        "budget_setting": {
            "epsilon": 0.2,
            "delt": 0.3,
        }
    }
    dpconfig = init_dpconfig(source_dpconfig)
    target_dpconfig = {
        "dp_method": "Gauss",
        "budget_setting": {
            "epsilon": 0.2,
            "delt": 0.3,
        }
    }
    assert dpconfig == target_dpconfig


def test_init_dpconfig_gauss_null_budget_setting():
    source_dpconfig = {
        "dp_method": "Gauss",
        "budget_setting": {
            "epsilon": None,
            "delt": None,
        }
    }
    dpconfig = init_dpconfig(source_dpconfig)
    target_dpconfig = {
        "dp_method": "Gauss",
        "budget_setting": {
            "epsilon": 0.9,
            "delt": 1e-8,
        }
    }
    assert dpconfig == target_dpconfig


def test_dpsql_init_dpconfig():
    dpsql_instance = DPSQL()
    target_dpconfig = {
        "dp_method": "Laplace",
        "budget_setting": {
            "epsilon": 0.9,
            "delt": 0,
        }
    }
    dpconfig = dpsql_instance.context.get_context("dpconfig")
    assert dpconfig == target_dpconfig


def test_dp_method_correct_gauss():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Gauss",
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


def test_dp_method_correct_laplace():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "LAPLACE",
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


def test_dp_method_correct_None():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": None,
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


def test_algorithm_param_extra_null():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_dp_method_error():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "other",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_err = json.loads(res)
    print("json_err:", json_err)
    standard = {"status": {"code": 1, "Message": "('param dp method Error', 'U9001')"}}
    assert json_err == standard


def test_budget_setting_correct_gauss():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-9,
            }
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


def test_null_budget_setting_correct_gauss():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": None,
                "delt": None,
            }
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


def test_budget_setting_correct_laplace():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Laplace",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-9,
            }
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


def test_dp_method_correct_laplace_join():
    sql = 'select count(*) as num from menu inner join menu_page on menu.id = menu_page.menu_id join menu_item on menu_item.menu_page_id = menu_page.id'
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Laplace",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-9,
            }
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
    # test_init_dpconfig_null()
    # test_init_dpconfig_gauss()
    # test_init_dpconfig_gauss_null_budget_setting()
    # test_dpsql_init_dpconfig()
    # test_dp_method_correct_gauss()
    # test_dp_method_correct_laplace()
    # test_dp_method_correct_laplace()
    # test_dp_method_correct_None()
    test_dp_method_correct_laplace_join()
    # test_algorithm_param_extra_null()
    # test_dp_method_error()
    # test_budget_setting_correct_gauss()
    # test_budget_setting_correct_laplace()
    # test_null_budget_setting_correct_gauss()
