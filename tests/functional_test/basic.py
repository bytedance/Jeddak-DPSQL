import requests

from tests.config.load_config import load_config

function_config = load_config("function_test.ini", "basic_test")


def request_get(route_path, args):
    config = get_config("server")
    host = config["host"]
    port = config["port"]
    url = "http://%s:%s/%s" % (host, port, route_path)
    headers = {"content-type": "application/json"}
    r = requests.get(url, json=args, headers=headers)
    return r.text


def request_post(route_path, args):
    config = get_config("server")
    host = config["host"]
    port = config["port"]
    url = "http://%s:%s/%s" % (host, port, route_path)
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=args, headers=headers)
    return r.text


def request_put(route_path, args):
    config = get_config("server")
    host = config["host"]
    port = config["port"]
    url = "http://%s:%s/%s" % (host, port, route_path)
    headers = {"content-type": "application/json"}
    r = requests.put(url, json=args, headers=headers)
    return r.text


def request_delete(route_path, args):
    config = get_config("server")
    host = config["host"]
    port = config["port"]
    url = "http://%s:%s/%s" % (host, port, route_path)
    headers = {"content-type": "application/json"}
    r = requests.delete(url, json=args, headers=headers)
    return r.text


def get_config(section):
    config = load_config("conf.ini", section)
    return config


if __name__ == "__main__":
    args = {"sql": "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20",
            "dbconfig": {
                "reader": "clickhouse",
                "host": function_config.get("ip"),
                "database": "default",
            },
            "queryconfig": {
                "traceid": "traceid",
            }
            }
    route_path = "/api/v1/query"
    res = request_post(route_path, args)
    print(res)
    print(get_config("clickhouse"))
    print(get_config("hivereader"))
