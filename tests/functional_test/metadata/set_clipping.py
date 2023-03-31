from time import sleep

from tests.functional_test.basic import request_put, get_config
from metadata.storage.metadata_bean_manager import get_column


def set_clipping(prefix, db_name, table_name, column_name, clipping_info):
    args = {
        "prefix": prefix,
        "db_name": db_name,
        "table_name": table_name,
        "column_name": column_name,
        "clipping_info": clipping_info
    }
    route_path = "/api/v1/metadata/set_clipping"
    r = request_put(route_path, args)
    return r


if __name__ == "__main__":
    config = get_config("clickhouse")
    prefix = config["host"]
    db_name = config["database"]
    table_name = "dish"
    column_name = "id"

    # clipping info
    clipping_info = {
        "clipping_flag": 1,
        "clipping_upper": 15,
        "clipping_lower": 65
    }

    # before update
    print("---------before update-----------")
    column_info = get_column(prefix, db_name, table_name, column_name)
    print(column_info)

    # update, Sleep time depends on when function set_clipping finishes executing
    set_clipping(prefix, db_name, table_name, column_name, clipping_info)
    sleep(5)

    # after update
    print("---------after update-----------")
    column_info = get_column(prefix, db_name, table_name, column_name)
    print(column_info)
