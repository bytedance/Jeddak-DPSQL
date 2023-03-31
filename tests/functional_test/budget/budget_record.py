from tests.functional_test.basic import request_post, get_config


def test_dp_method_correct_gauss():
    data_source = "clickhouse"
    config = get_config(data_source)
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": {
            "reader": data_source,
            "host": config["host"],
            "database": config["database"],
            "port": config["port"],
        },
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-5,
            }
        },
        "extra": {
            "debug": True,
        }
    }

    route_path = "/api/v1/query"
    res = request_post(route_path, key)
    print(res)


def test_dp_method_correct_laplace():
    data_source = "clickhouse"
    config = get_config(data_source)
    # sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    # sql = "select count(menu_id), sum(page_number) from menu_page group by menu_id limit 20"
    # sql = '''
    #         select avg(menu_id) from menu_page group by menu_id limit 20
    #         '''
    # sql = '''
    #             select avg(menu_id) as avg_mm from menu_page group by menu_id limit 20
    #             '''
    sql = '''
            select sum(menu_id) from menu_page group by menu_id limit 20
            '''
    key = {
        "sql": sql,
        "dbconfig": {
            "reader": data_source,
            "host": config["host"],
            "database": config["database"],
            "port": config["port"],

        },
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Laplace",
            "budget_setting": {
                "epsilon": 10.0,
                "delt": 1e-5,
            }
        },
        "extra": {
            "debug": True,
        }
    }
    route_path = "/api/v1/query"
    res = request_post(route_path, key)
    print(res)


if __name__ == '__main__':
    # test_dp_method_correct_gauss()
    test_dp_method_correct_laplace()
