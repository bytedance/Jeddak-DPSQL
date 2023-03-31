from dbaccess.hive.hive import HiveDataAccess
from tests.unit_test.utils import HIVE_DB_CONFIG, QUERTCONFIG


# Native hive execution test
def test_hive_reader():
    sql = 'select * from user_info limit 10'
    reader = HiveDataAccess()
    res = reader.execute(sql, HIVE_DB_CONFIG, QUERTCONFIG)
    col_types = res.get_type()
    standard = ['BIGINT', 'STRING', 'STRING', 'INT', 'INT', 'STRING', 'STRING', 'STRING', 'STRING']
    assert col_types == standard
