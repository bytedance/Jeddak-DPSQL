from metadata.converter.clickhouse import ClickhouseTypeConverter
from metadata.converter.hive import HiveTypeConverter


def test_clickhouse_op_dbtype():
    converter = ClickhouseTypeConverter()
    assert (converter.op_dbtype("%", "", "") == "UInt64")
    assert (converter.op_dbtype("/", "", "") == "Float64")
    assert (converter.op_dbtype("*", "UInt8", "UInt8") == "UInt8")
    assert (converter.op_dbtype("*", "UInt16", "Int32") == "Int32")
    assert (converter.op_dbtype("*", "UInt64", "Int32") == "Int64")
    assert (converter.op_dbtype("*", "UInt32", "Float64") == "Float64")

    assert (converter.op_dbtype("+", "UInt8", "UInt8") == "UInt8")
    assert (converter.op_dbtype("+", "UInt16", "Int32") == "Int32")
    assert (converter.op_dbtype("+", "UInt64", "Int32") == "Int64")
    assert (converter.op_dbtype("+", "UInt32", "Float64") == "Float64")

    assert (converter.op_dbtype("-", "UInt8", "UInt8") == "UInt8")
    assert (converter.op_dbtype("-", "UInt16", "Int32") == "Int32")
    assert (converter.op_dbtype("-", "UInt64", "Int32") == "Int64")
    assert (converter.op_dbtype("-", "UInt32", "Float64") == "Float64")


def test_hive_op_db_type():
    converter = HiveTypeConverter()
    assert (converter.op_dbtype("/", "", "") == "double")
    assert (converter.op_dbtype("div", "", "") == "integer")

    assert (converter.op_dbtype("+", "tinyint", "tinyint") == "tinyint")
    assert (converter.op_dbtype("+", "tinyint", "smallint") == "smallint")
    assert (converter.op_dbtype("+", "smallint", "tinyint") == "smallint")

    assert (converter.op_dbtype("-", "tinyint", "tinyint") == "tinyint")
    assert (converter.op_dbtype("-", "tinyint", "smallint") == "smallint")
    assert (converter.op_dbtype("-", "smallint", "tinyint") == "smallint")

    assert (converter.op_dbtype("*", "tinyint", "tinyint") == "tinyint")
    assert (converter.op_dbtype("*", "tinyint", "smallint") == "smallint")
    assert (converter.op_dbtype("*", "smallint", "tinyint") == "smallint")
