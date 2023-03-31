from time import sleep

from tests.functional_test.basic import get_config, request_put
from metadata.storage.metadata_bean_manager import query_meta


def meta_update(table_name, db_config, db_type):
    args = {
        "db_config": db_config,
        "table_name": table_name,
        "db_type": db_type
    }
    route_path = "/api/v1/metadata/update"
    r = request_put(route_path, args)
    print(r)
    return r


if __name__ == "__main__":
    # clickhouse
    config = get_config("clickhouse")
    table_name = "dish"
    db_type = "clickhouse"
    db_config = {
        "host": config["host"],
        "database": config["database"],
        "username": config["username"],
        "password": config["password"]
    }
    # before update
    prefix = config["host"]
    db_name = config["database"]

    print("________before update_____________")
    print(query_meta(prefix, db_name, table_name))

    # update, Sleep time depends on when function meta_update finishes executing
    meta_update(table_name, db_config, db_type)
    sleep(30)

    # after update
    print("after update_____________")
    print(query_meta(prefix, db_name, table_name))
