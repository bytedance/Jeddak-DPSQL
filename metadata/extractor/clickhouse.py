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
import time
from dbaccess.clickhouse.clickhouse import ClickHouseDataAccess
from exception.enum.meradata_errors_enum import MetaDataErrors
from metadata.converter.clickhouse import ClickhouseTypeConverter
from metadata.extractor.base import MetaExtractor
from exception.errors import MetaDataError
import re
import uuid


class ClickhouseMetaExtractor(MetaExtractor):
    def __init__(self, reader=None):
        super(ClickhouseMetaExtractor, self).__init__()
        self.reader = reader
        self.Engine = "clickhouse"

    def set_config(self, db_config=None):
        if db_config is None:
            raise MetaDataError(MetaDataErrors.EXTRACTOR_META_ERROR.value, "db_config can not be None")
        Config = {
            "db_config": db_config,
            "query_config": {}
        }
        Config["query_config"]["traceid"] = "query_id"
        Config["query_config"]["taskId"] = str(time.time())
        self.db_config = Config["db_config"]
        self.query_config = Config["query_config"]

    def _get_query_answer(self, sql=None):
        self.query_config["traceid"] = str(uuid.uuid1())
        try:
            logging.info("tracing-sql-execution-ClickhouseMetaExtractor: traceid = %s, sql = %s start_execute",
                         self.query_config["traceid"], sql)
            res = self.reader.execute(sql, self.db_config, self.query_config)
            return res
        except Exception as err:
            logging.exception(
                "tracing-sql-execution-ClickhouseMetaExtractor: traceid = %s, sql = %s execute failed, err = %s",
                self.query_config["traceid"], sql, str(err))
            raise MetaDataError(MetaDataErrors.EXTRACTOR_META_ERROR.value,
                                "fail in answering MetaExtract SQL:" + str(err))

    def _get_col_info_list(self):
        sql = "SELECT * FROM {DBName}.{TableName} limit 0".format(DBName=self.DBName, TableName=self.TableName)
        res = self._get_query_answer(sql)
        col_DBtype_list = res.col_type
        col_name_list = list(res.result[0])
        formated_col_DBtype_list = list(map(format_clickhouse_type, col_DBtype_list))
        col_type_list = list(map(ClickhouseTypeConverter().dbtype_to_type, formated_col_DBtype_list))
        return formated_col_DBtype_list, col_type_list, col_name_list

    def _get_max_fre(self, ColName=None):
        sql_base = '''
                        select max(FRE) as maxFre
                        from
                            (select
                                {ColName}, count({ColName}) as FRE
                            from
                                {DBName}.{TableName}
                            group by {ColName})
                    '''
        sql = sql_base.format(DBName=self.DBName, TableName=self.TableName, ColName=ColName)
        res = self._get_query_answer(sql)
        return res.result[1][0]

    def _get_max_min(self, ColName=None):
        sql_base = "select max({ColName}) as upperbound, min({ColName}) as lowerbound from {DBName}.{TableName}"
        sql = sql_base.format(DBName=self.DBName, TableName=self.TableName, ColName=ColName)
        res = self._get_query_answer(sql)
        return res.result[1][0], res.result[1][1]

    def _check_map_type(self, DBtype=None):
        pattern = re.compile(r"Map\((.*)\)")
        result = pattern.search(DBtype)
        if result is not None:
            pure_type = result.group(1)
            key_val_DBtype = re.split(r"[,\s]+", pure_type)
            key_DBtype, val_DBtype = key_val_DBtype[0], key_val_DBtype[-1]
            type_converter = ClickhouseTypeConverter()
            key_type = type_converter.dbtype_to_type(key_DBtype)
            val_type = type_converter.dbtype_to_type(val_DBtype)
            if key_type in ["string"] and val_type in ['int', 'float']:
                return True
            else:
                return False
        else:
            raise MetaDataError(MetaDataErrors.VERIFY_MAP_TYPE_ERROR.value, "cannot check the map type!")

    def _get_map_key_list(self, ColName=None):
        sql_base = "SELECT distinct mapKeys({ColName}) FROM {DBName}.{TableName}"
        sql = sql_base.format(DBName=self.DBName, TableName=self.TableName, ColName=ColName)
        res = self._get_query_answer(sql)
        if len(res.result) > 1:
            key_array_list = res.result[1:]
            key_set = set()
            for key_array in key_array_list:
                key_set.update(key_array[0])
            key_list = list(key_set)
            key_list.sort()
            return key_list
        else:
            raise MetaDataError(MetaDataErrors.GET_MAPKEY_ERROR.value, "cannot get mapKeys for the map column!")

    def _get_val_extr_list(self, ColName=None, key_list=None, extr=None):
        key_num = len(key_list)
        SQL_extr = ""
        SQL_dict = {"EX": extr,
                    "ColName": ColName,
                    "Q": "\'",
                    "LCB": "{",
                    "RCB": "}",
                    "Key": ""}
        for i in range(key_num):
            if i == 0:
                SQL_dict["Key"] = key_list[0]
                SQL_extr = "{EX}({ColName}{LCB}{Q}{Key}{Q}{RCB}) AS {Key}".format(**SQL_dict)
            else:
                SQL_dict["Key"] = key_list[i]
                SQL_extr = SQL_extr + ", {EX}({ColName}{LCB}{Q}{Key}{Q}{RCB}) AS {Key}".format(**SQL_dict)
        sql_base = " from {DBName}.{TableName}".format(DBName=self.DBName, TableName=self.TableName)
        sql = "select " + SQL_extr + sql_base
        res = self._get_query_answer(sql)
        return res.result[1]

    def execute_extraction(self, DBName=None, TableName=None):
        self.DBName = DBName
        self.TableName = TableName
        self.metadata_dict = {"engine": self.Engine, "database": DBName, "tables": []}
        table_dict = {"tablename": TableName, "columns": {}}
        col_DBtype_list, col_type_list, col_name_list = self._get_col_info_list()
        col_num = len(col_DBtype_list)
        for i in range(col_num):
            DBtype = col_DBtype_list[i]
            col_type = col_type_list[i]
            col_name = col_name_list[i]
            column_dict = {"type": DBtype}
            if col_type in ["int"]:
                max_val, min_val = self._get_max_min(col_name)
                max_fre = self._get_max_fre(col_name)
                column_dict["upper"] = max_val
                column_dict["lower"] = min_val
                column_dict["max_fre"] = max_fre
            elif col_type in ["float"]:
                max_val, min_val = self._get_max_min(col_name)
                column_dict["upper"] = max_val
                column_dict["lower"] = min_val
            elif col_type in ["map"]:
                if self._check_map_type(DBtype):
                    key_list = self._get_map_key_list(col_name)
                    valMax_list = self._get_val_extr_list(col_name, key_list, "max")
                    valMin_list = self._get_val_extr_list(col_name, key_list, "min")
                    key_metas = []
                    key_num = len(key_list)
                    for i in range(key_num):
                        key_meta = {"name": key_list[i], "upper": valMax_list[i], "lower": valMin_list[i]}
                        key_metas.append(key_meta)
                    column_dict["key_metas"] = key_metas
            table_dict["columns"][col_name] = column_dict
        self.metadata_dict["tables"].append(table_dict)


def format_clickhouse_type(DBtype=None):
    pattern = re.compile(r"Nullable\((\S*)\)")
    result = pattern.search(DBtype)
    formated_DBtype = DBtype
    if result is not None:
        pure_type = result.group(1)
        formated_DBtype = pattern.sub(pure_type, DBtype)
    return formated_DBtype


def gen_meta_for_clickhouse(DBName=None, TableName=None, DBConfig=None):
    try:
        ch_reader = ClickHouseDataAccess()
        meta_extractor = ClickhouseMetaExtractor(ch_reader)
        meta_extractor.set_config(DBConfig)
        meta_extractor.execute_extraction(DBName, TableName)
        return meta_extractor.metadata_dict
    except Exception as err:
        raise MetaDataError(MetaDataErrors.CLICKHOUSE_META_EXCEPTION.value, "DBName-%s, TableName-%s, err-%s" % (DBName, TableName, str(err)))
