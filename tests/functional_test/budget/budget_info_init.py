from tests.functional_test.basic import get_config, request_post


def meta_and_budget_generate(table_name, db_config, db_type):
    args = {
        "db_config": db_config,
        "table_name": table_name,
        "db_type": db_type
    }
    route_path = "/api/v1/metadata/generate"
    r = request_post(route_path, args)
    print(r)


if __name__ == "__main__":
    # # clickhouse
    # config = get_config("clickhouse")
    # table_name = "dish"
    # db_type = "clickhouse"
    # db_config = {
    #     "host": config["host"],
    #     "database": config["database"],
    #     "username": config["username"],
    #     "password": config["password"]
    # }

    # hive
    config = get_config("hivereader")
    table_name = "user_info"
    db_type = "hive"
    db_config = {
        "host": config["host"],
        "database": config["database"],
        # "username": config["username"],
        # "password": config["password"]
    }

    # # generate, Sleep time depends on when function meta_generate finishes executing
    meta_and_budget_generate(table_name, db_config, db_type)
