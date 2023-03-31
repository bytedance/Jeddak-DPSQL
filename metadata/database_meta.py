# Copyright (2023) Beijing Volcano Engine Technology Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import re
from dataclasses import dataclass
from exception.enum.meradata_errors_enum import MetaDataErrors
from metadata.converter.clickhouse import ClickhouseTypeConverter
from exception.errors import MetaDataError
from metadata.converter.hive import HiveTypeConverter


class DatabaseMetadata:
    """metadabse of database"""

    def __init__(self, dbname, tables, engine):
        """Instantiate a metadata object with information about tabular data sources

        :param tables: A list of TableMetadata descriptions
        :param engine: The name of the database engine used to query these tables.  Used for engine-
            specific name escaping and comparison.  Set to None to use default semantics.
        """
        self.m_tables = tables
        self.engine = engine if engine is not None else "Unknown"
        self.dbname = dbname
        self.table_id_dict = {}

    def __str__(self):
        return "\n\n".join([str(table) for table in self.m_tables])

    def tables(self):
        return self.m_tables

    def _get_table_key(self, table):
        extra_match = ""
        if table.extra_match is not None:
            extra_match = "*" + str(table.extra_match["appid"])
        if table.dbname is not None:
            return table.dbname + "*" + table.name + extra_match
        else:
            raise ValueError("need to revise table_key for %s" % table.dbname)

    @staticmethod
    def from_dict(meta_dict):
        """Load the metadata from a dict object"""
        loader = MetaInMemLoader()
        return loader.from_dict(meta_dict)


class TableMetadata:
    """Information about a single tabular data source"""

    def __init__(
            self,
            dbname,
            name,
            columns,
            rowcount=0,
            extra_match={}
    ):
        """Instantiate information about a tabular data source.

        :param dbname: database name
        :param name: The table name that will be used by SQL queries to reference data
            in this table.
        :param rowcount: The rough number of rows in this table.  Should not be the exact number, and does not need to be accurate
        :param columns: A list of Column objects with information about each column in the table.
        """
        self.dbname = dbname
        self.name = name
        self.rowcount = rowcount
        self.extra_match = extra_match

        self.m_columns = dict([(c.name, c) for c in columns])

    def __str__(self):
        return (str(self.dbname)
                + "."
                + str(self.name)
                + " ["
                + str(self.rowcount)
                + " rows]\n\t"
                + "\n\t".join([str(self.m_columns[col]) for col in self.m_columns.keys()])
                )

    def key_cols(self):
        return [
            self.m_columns[name]
            for name in self.m_columns.keys()
            if self.m_columns[name].is_key is True
        ]

    def columns(self):
        return [self.m_columns[name] for name in self.m_columns.keys()]

    def __iter__(self):
        return self.columns()

    def table_name(self):
        return (self.dbname + "." if len(self.dbname.strip()) > 0 else "") + self.name


@dataclass
class Column:
    name: str
    is_key: bool = False
    bounded: bool = False
    _dbtype: str = "unknow"
    max_fre: int = None

    def dbtype(self):
        return self._dbtype


@dataclass
class String(Column):
    _dbtype: str = "string"

    def __str__(self):
        return ("*" if self.is_key else "") + str(self.name)

    def type(self):
        return "string"


@dataclass
class Boolean(Column):
    """A column with True/False data"""
    _dbtype: str = "boolean"

    def __str__(self):
        return ("*" if self.is_key else "") + str(self.name) + " [boolean]"

    def type(self):
        return "boolean"


@dataclass
class DateTime(Column):
    """A date/time column"""
    _dbtype: str = "datetime"

    def __str__(self):
        return ("*" if self.is_key else "") + str(self.name) + " [datetime]"

    def type(self):
        return "datetime"


@dataclass
class Int(Column):
    """A column with integer data"""
    _dbtype: str = "int"
    minval: int = None
    maxval: int = None
    clipping_flag: int = None
    unbounded = minval is None or maxval is None

    def __str__(self):
        bounds = "unbounded" if self.unbounded else str(self.minval) + "," + str(self.maxval)
        return ("*" if self.is_key else "") + str(self.name) + " [int] (" + bounds + ")"

    def type(self):
        return "int"


@dataclass
class Float(Column):
    """A floating point column"""
    _dbtype: str = "float"
    minval: int = None
    maxval: int = None
    clipping_flag: int = None
    unbounded = minval is None or maxval is None

    def __str__(self):
        bounds = "unbounded" if self.unbounded else str(self.minval) + "," + str(self.maxval)
        return ("*" if self.is_key else "") + str(self.name) + " [float] (" + bounds + ")"

    def type(self):
        return "float"


class Array:
    """A column with array data. TODO: rewrite with dataclass"""

    def __init__(self, name, element_type, element_dbtype, is_key=False, bounded=False, dbtype="array", max_fre=None):
        self.name = name
        self.is_key = is_key
        self.bounded = bounded
        self._dbtype = dbtype
        self.max_fre = max_fre
        self.element_type = element_type
        self.element_dbtype = element_dbtype

    def __str__(self):
        return ("*" if self.is_key else "") + str(self.name) + " [array( " + self.element_type + ")]"

    def dbtype(self):
        return self._dbtype

    def type(self):
        return "array"


class Map:
    """A column with array data. TODO: rewrite with dataclass"""

    def __init__(self, name, key_type, key_dbtype, value_type, value_dbtype, is_key=False, bounded=False, dbtype="map", max_fre=None):
        self.name = name
        self.key_type = key_type
        self.key_dbtype = key_dbtype
        self.value_type = value_type
        self.value_dbtype = value_dbtype
        self.is_key = is_key
        self.bounded = bounded
        self.key_metas = []
        self._dbtype = dbtype
        self.max_fre = max_fre
        self.key_metas_event_name_dict = {}

    def __str__(self):
        return ("*" if self.is_key else "") + str(self.name) + " [map(" + self.key_type + ", " + self.value_type + ")]"

    def add_key_meta(self, key_meta):
        self.key_metas.append(key_meta)

    def add_key_meta_event_name_dict(self, key_meta=None, id=None):
        event_name_cont = key_meta["event"] + "*" + key_meta["name"]
        self.key_metas_event_name_dict[event_name_cont] = id

    def get_key_meta(self, key):
        for m in self.key_metas:
            if m["name"] == key:
                return m

    def dbtype(self):
        return self._dbtype

    def type(self):
        return "map"


class MetaInMemLoader:
    def __init__(self):
        pass

    def from_dict(self, in_dict):
        engine = in_dict["engine"]
        db_name = in_dict['database']
        tables = in_dict["tables"]
        if engine == "clickhouse":
            self.type_converter = ClickhouseTypeConverter()
        elif engine == "hive":
            self.type_converter = HiveTypeConverter()
        else:
            raise MetaDataError(MetaDataErrors.CONVERTER_NOT_EMPLEMENT.value, "type converter of %s engine is not implemented" % (engine))

        table_metas = []

        for table in tables:
            table_metas.append(self.load_table(db_name, table["tablename"], table))

        return DatabaseMetadata(db_name, table_metas, engine)

    def load_table(self, dbname, table, t):
        rowcount = int(t["rows"]) if "rows" in t else 0
        extra_mattch = t["extra_match"] if "extra_match" in t else None

        columns_meta = t["columns"]
        columns = []
        colnames = [
            cn
            for cn in columns_meta.keys()
        ]
        for column in colnames:
            columns.append(self.load_column(column, columns_meta[column]))

        return TableMetadata(
            dbname,
            table,
            columns,
            rowcount,
            extra_mattch
        )

    def load_column(self, column, c):
        is_key = False if "private_id" not in c else bool(c["private_id"])
        bounded = False if "bounded" not in c else bool(c["bounded"])
        dbtype = c["type"]
        _type = self.type_converter.dbtype_to_type(dbtype)
        max_fre = int(c["max_fre"]) if "max_fre" in c else None
        clipping_flag = c["clipping_flag"] if "clipping_flag" in c else None
        clipping_upper = float(c["clipping_upper"]) if "clipping_upper" in c else None
        clipping_lower = float(c["clipping_lower"]) if "clipping_lower" in c else None
        if _type == "boolean":
            return Boolean(column, is_key, bounded, dbtype, max_fre)
        elif _type in ["datetime", "date"]:
            return DateTime(column, is_key, bounded, dbtype, max_fre)
        elif _type in ["int", "uint32", "uint64"]:
            minval = int(c["lower"]) if "lower" in c else None
            maxval = int(c["upper"]) if "upper" in c else None
            if clipping_flag:
                minval = clipping_lower
                maxval = clipping_upper
            return Int(column, is_key, bounded, dbtype, max_fre, minval, maxval, clipping_flag=clipping_flag)
        elif _type == "float":
            minval = float(c["lower"]) if "lower" in c else None
            maxval = float(c["upper"]) if "upper" in c else None
            if clipping_flag:
                minval = clipping_lower
                maxval = clipping_upper
            return Float(column, is_key, bounded, dbtype, max_fre, minval, maxval, clipping_flag=clipping_flag)
        elif _type == "string":
            # card = int(c["cardinality"]) if "cardinality" in c else 0
            return String(column, is_key, bounded, dbtype, max_fre)
        elif _type == "array":
            match = re.match(r"Array\(\s*(\w+)\s*\)", dbtype)
            ele_dbtype = match.group(1)
            ele_type = self.type_converter.dbtype_to_type(ele_dbtype)
            return Array(column, ele_type, ele_dbtype, is_key, bounded, dbtype, max_fre)
        elif _type == "map":
            match = re.match(r"Map\(\s*(\w+)\s*,\s*([\w\(\)]+)\s*\)", dbtype)
            key_dbtype = match.group(1)
            key_type = self.type_converter.dbtype_to_type(key_dbtype)
            value_dbtype = match.group(2)
            value_type = self.type_converter.dbtype_to_type(value_dbtype)
            key_metas = c["key_metas"] if "key_metas" in c else None
            m = Map(column, key_type, key_dbtype, value_type, value_dbtype, is_key, bounded, dbtype, max_fre)
            if key_metas:
                id = 0
                for km in key_metas:
                    if km.get("event") is None:
                        km["event"] = "any_event"
                    m.add_key_meta(km)
                    m.add_key_meta_event_name_dict(km, id)
                    id += 1
            return m
        else:
            logging.error("dpaccess-internal-Unknown column type for column {0}: {1}".format(column, c))
            raise MetaDataError(MetaDataErrors.UNKNOW_COLUMN_ERROR.value, "Unknown column type for column")

    def to_dict(self, db_metadata):
        tables = []
        for t in db_metadata.tables():
            table = {}
            table["tablename"] = t.name
            table["columns"] = {}
            if t.extra_match is not None:
                table["extra_match"] = t.extra_match
            columns = table["columns"]
            tables.append(table)
            for c in t.columns():
                cname = c.name
                if cname in columns:
                    logging.error("dpaccess-internal-Duplicate column name {0} in table {1}".format(cname, t.name))
                    raise MetaDataError(MetaDataErrors.DUP_COL_NAME_ERROR.value, "Duplicate column name in table")
                columns[cname] = {}
                column = columns[cname]
                if hasattr(c, "bounded") and c.bounded is True:
                    column["bounded"] = c.bounded
                if hasattr(c, "card"):
                    column["cardinality"] = c.card
                if hasattr(c, "minval") and c.minval is not None:
                    column["lower"] = c.minval
                if hasattr(c, "maxval") and c.maxval is not None:
                    column["upper"] = c.maxval
                if hasattr(c, "max_fre") and c.max_fre is not None:
                    column["max_fre"] = c.max_fre
                if c.is_key is not None and c.is_key is True:
                    column["private_id"] = c.is_key

                column["type"] = c.dbtype()
                if type(c) is Map:
                    if len(c.key_metas) > 0:
                        column["key_metas"] = c.key_metas
        db = {}
        db["tables"] = tables
        db["engine"] = db_metadata.engine
        db["database"] = db_metadata.dbname
        return db
