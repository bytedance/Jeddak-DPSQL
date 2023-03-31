from time import sleep

from tests.functional_test.basic import get_config, request_post
from metadata.storage.metadata_bean_manager import query_meta, if_exist_meta_without_cache


def meta_generate(table_name, db_config, db_type):
    args = {
        "db_config": db_config,
        "table_name": table_name,
        "db_type": db_type
    }
    route_path = "/api/v1/metadata/generate"
    r = request_post(route_path, args)
    print(r)
    return r


if __name__ == "__main__":
    # clickhouse
    config = get_config("clickhouse")
    # table_name = "dish"
    table_name = "menu_item"
    db_type = "clickhouse"
    db_config = {
        "host": config["host"],
        "database": config["database"],
        "username": config["username"],
        "password": config["password"]
    }

    # # hive
    # config = get_config("hivereader")
    # table_name = "us_accidents_dec21_updated"
    # db_type = "hive"
    # db_config = {
    #     "host": config["host"],
    #     "database": config["database"],
    #     # "username": config["username"],
    #     # "password": config["password"]
    # }

    # before generate
    print("________before genarete,if_exist meta query result_____________")
    prefix = config["host"]
    db_name = config["database"]
    if_exist = if_exist_meta_without_cache(prefix, db_name, table_name)
    print(if_exist)

    # generate, Sleep time depends on when function meta_generate finishes executing
    meta_generate(table_name, db_config, db_type)
    sleep(60)

    # after generate
    print("after genarete, if_exist meta query result_____________")
    if_exist = if_exist_meta_without_cache(prefix, db_name, table_name)
    print(if_exist)
    print("meta query result_____________")
    print(query_meta(prefix, db_name, table_name))
