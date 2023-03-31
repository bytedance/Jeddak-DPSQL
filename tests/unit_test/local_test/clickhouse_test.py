from dbaccess.clickhouse.clickhouse import ClickHouseDataAccess
from tests.unit_test.utils import QUERTCONFIG, DBCONFIG_FOR_CK

CLICKHOUSE_READER = ClickHouseDataAccess()


# Native ck execution test
def test_clickhouse_reader():
    sql = "select * from menu_page limit 10"
    res = CLICKHOUSE_READER.execute(sql, DBCONFIG_FOR_CK, QUERTCONFIG)
    print(res)
    col_types = res.get_type()
    standard = ['UInt32', 'UInt32', 'UInt16', 'String', 'UInt16', 'UInt16', 'UUID']
    assert col_types == standard
