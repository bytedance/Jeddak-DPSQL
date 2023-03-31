from enum import Enum

from parser.ast.base import Seq
from parser.ast.visitor.tree_visitor import VisitorOrder


class BaseType:
    """Enum BaseType"""
    def accept(self, visitor, order=VisitorOrder.FORWARD):
        if visitor is None:
            raise Exception("visitor cannot be none")
        visitor.preVisit(self)
        self.accept0(visitor, order)
        visitor.postVisit(self)

    def accept0(self, visitor, order):
        pass


# https://clickhouse.tech/docs/en/sql-reference/data-types/
class SqlNumberType(BaseType, Enum):
    INF = 10001
    NAN = 10002
    Int8 = 10011
    Int16 = 10012
    Int32 = 10013
    Int64 = 10014
    Int128 = 10015
    Int256 = 10016
    UInt8 = 10017
    UInt16 = 10018
    UInt32 = 10019
    UInt64 = 10020
    UInt128 = 10021
    UInt256 = 10022
    Float32 = 10031
    Float64 = 10032


class HiveSqlNumberType(BaseType, Enum):
    TINYINT = 10101
    SMALLINT = 10102
    INT = 10103
    BIGINT = 10104
    FLOAT = 10105
    DOUBLE = 10106
    DECIMAL = 10107
    NUMERIC = 10108


class SqlDecimalType(BaseType):
    def __init__(self):
        super(SqlDecimalType, self).__init__()
        self.type_name = None
        self.args = Seq(self)

    def __str__(self):
        return str(self.type_name) + "(" + ",".join(str(c) for c in self.args) + ")"


class SqlBooleanType(BaseType):
    def __init__(self):
        super(SqlBooleanType, self).__init__()


class SqlStringType(BaseType):
    def __init__(self):
        super(SqlStringType, self).__init__()


class SqlFixedstringType(BaseType):
    def __init__(self):
        super(SqlFixedstringType, self).__init__()


class CommonWithParamType(BaseType):
    def __init__(self):
        super(CommonWithParamType, self).__init__()
        self.type = None
        self.args = Seq(self)

    def __str__(self):
        return str(self.type) + "(" + ",".join(str(c) for c in self.args) + ")"

    def clone(self):
        return self

    def dbtype(self, converter):
        return self.args.dbtype(converter)


class SqlUUIDType(BaseType):
    def __init__(self):
        super(SqlUUIDType, self).__init__()


class SqlDateType(BaseType):
    Date = 1
    Date32 = 2


class SqlDateTimeType(BaseType):
    DateTime = 1
    DateTime64 = 2


# Enum8('hello' = 1, 'world' = 2)
class SqlEnumType(BaseType):
    def __init__(self):
        super(SqlEnumType, self).__init__()
        self.enum_type = None
        # EnumExpr
        self.args = Seq(self)

    def __str__(self):
        return str(self.enum_type) + "(" + ",".join(str(c) for c in self.args) + ")"


# https://clickhouse.tech/docs/en/sql-reference/data-types/lowcardinality/
class SqlLowCardinality(BaseType):
    def __init__(self):
        super(SqlLowCardinality, self).__init__()
        self.type = None


# https://clickhouse.tech/docs/en/sql-reference/data-types/aggregatefunction/
class SqlAggregateFunctionType(BaseType):
    def __init__(self):
        super(SqlAggregateFunctionType, self).__init__()


# https://clickhouse.tech/docs/en/sql-reference/data-types/nested-data-structures/nested/
# Nested
#     (
#         ID UInt32,
#         Serial UInt32,
#         EventTime DateTime,
#         Price Int64,
#         OrderID String,
#         CurrencyID UInt32
#     )
class SqlNestedType(BaseType):
    def __init__(self):
        super(SqlNestedType, self).__init__()
        self.out_type_name = None
        # TokenDefinitionExpr
        self.inner_type_seq = Seq(self)

    def __str__(self):
        return str(self.out_type_name) + " ( " + ",".join(str(c) for c in self.inner_type_seq)


# Array, Tuple
class SqlComplexType(BaseType):
    def __init__(self):
        super(SqlComplexType, self).__init__()
        self.out_type_name = None
        self.inner_args = Seq(self)

    def __str__(self):
        return str(self.out_type_name) + " ( " + ",".join(str(c) for c in self.inner_args) + " )"


# https://clickhouse.tech/docs/en/sql-reference/data-types/nullable/
class SqlNullableType(BaseType):
    def __init__(self):
        super(SqlNullableType, self).__init__()


# https://clickhouse.tech/docs/en/sql-reference/data-types/geo/
class SqlGeoType(BaseType):
    def __init__(self):
        super(SqlGeoType, self).__init__()


# https://clickhouse.tech/docs/zh/sql-reference/data-types/simpleaggregatefunction/
class SqlSimpleAggregateFunction(BaseType):
    def __init__(self):
        super(SqlSimpleAggregateFunction, self).__init__()


# https://clickhouse.tech/docs/en/sql-reference/data-types/map/
class SqlMapType(BaseType):
    def __init__(self):
        super(SqlMapType, self).__init__()
        self.key_type = None
        self.value_value = None
