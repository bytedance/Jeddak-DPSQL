from tests.functional_test.basic import request_get, get_config


def meta_query(prefix, db_name, table_name):
    args = {
        "prefix": prefix,
        "db_name": db_name,
        "table_name": table_name
    }
    route_path = "/api/v1/metadata/get"
    r = request_get(route_path, args)
    print(r)
    return r


if __name__ == "__main__":
    config = get_config("clickhouse")
    prefix = config["host"]
    db_name = "default"
    table_name = "dish"
    meta_query(prefix, db_name, table_name)
