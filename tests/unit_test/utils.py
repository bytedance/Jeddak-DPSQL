import subprocess
from dbaccess.clickhouse.clickhouse import ClickHouseDataAccess
from dbaccess.hive.hive import HiveDataAccess
from query_driver.dpsql import DPSQL
git_root_dir = subprocess.check_output("git rev-parse --show-toplevel".split(" ")).decode("utf-8").strip()

QUERTCONFIG = {
    "traceid": "traceid",
}

DBCONFIG_FOR_CK = {
    "reader": "clickhouse",
    "host": "your clickhouse ip",
    "database": "default",
}


HIVE_DB_CONFIG = {
    "reader": "hivereader",
    "database": "default",

    "host": "your clickhouse ip",
    "port": 10000,
}

CLICKHOUSE_READER = ClickHouseDataAccess()
HIVE_READER = HiveDataAccess()
# create dpsql
DPSQL_TEST = DPSQL()
