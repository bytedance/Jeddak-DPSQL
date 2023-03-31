from time import sleep

from tests.functional_test.basic import get_config, request_delete
from metadata.storage.metadata_bean_manager import if_exist_meta_without_cache


def delete_metadata(prefix, db_name, table_name):
    args = {
        "prefix": prefix,
        "db_name": db_name,
        "table_name": table_name
    }
    route_path = "/api/v1/metadata/delete"
    r = request_delete(route_path, args)
    print(r)
    return r


if __name__ == "__main__":
    config = get_config("hivereader")
    prefix = config["host"]
    db_name = config["database"]
    table_name = "user_info"

    # before delete
    print("________before delete, if_exist meta query result_____________")
    if_exist = if_exist_meta_without_cache(prefix, db_name, table_name)
    print(if_exist)

    # delete, Sleep time depends on when function delete_metadata finishes executing
    delete_metadata(prefix, db_name, table_name)
    sleep(30)

    # after delete
    print("________after delete, if_exist meta query result_____________")
    if_exist = if_exist_meta_without_cache(prefix, db_name, table_name)
    print(if_exist)
