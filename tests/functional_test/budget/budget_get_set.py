from tests.functional_test.basic import request_post, request_get


def budget_set():
    key = {
        "prefix": "1.1.1.3",
        "db_name": "test_db_1",
        "table_name": "test_table_2",
        "total_budget": 77777.0,
        "recover_cycle": 88,
        "exhausted_strategy": "reject",
    }

    route_path = "/api/v1/budget/set"
    r = request_post(route_path, key)
    print(r)


def budget_get():
    key = {
        # "prefix": "1.1.1.1",
        "db_name": "test_db",
        "table_name": "test_table",
    }

    route_path = "/api/v1/budget/get"
    r = request_get(route_path, key)
    print(r)


def budget_get_no_content():
    key = {
        "prefix": "1.1.1.33",
        "db_name": "test_db",
        "table_name": "test_table",
    }

    route_path = "/api/v1/budget/get"
    r = request_get(route_path, key)
    print(r)


if __name__ == '__main__':
    budget_get()
    # budget_get_no_content()
    # budget_set()
