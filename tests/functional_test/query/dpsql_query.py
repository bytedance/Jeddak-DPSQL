from dbaccess.reader_factory import reader_selector
from tests.functional_test.basic import request_post, get_config


def query_sql_noise(sql, data_source):
    config = get_config(data_source)
    key = {"sql": sql,
           "dbconfig": {
               "reader": data_source,
               "host": config["host"],
               "database": config["database"],
               "port": config["port"],
               "username": config["username"],
               "password": config["password"]
           },
           "queryconfig": {
               "traceid": "traceid",
           },
           "extra": {
               "debug": True
           }
           }
    route_path = "/api/v1/query"
    res = request_post(route_path, key)
    return res


def source_query(sql, datasource):
    reader = reader_selector(datasource)
    config = get_config(datasource)
    db_config = {
        "reader": datasource,
        "host": config["host"],
        "database": config["database"],
        "port": config["port"],

    }
    res = reader.execute(sql, db_config, {})
    return res


if __name__ == "__main__":
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    section = "clickhouse"
    res = query_sql_noise(sql, section)
    print(res)
    res2 = source_query(sql, section)
    print(res2)
