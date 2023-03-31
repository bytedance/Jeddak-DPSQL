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
import uuid
from dbaccess.hive.hive import HiveDataAccess
from exception.enum.meradata_errors_enum import MetaDataErrors
from exception.errors import MetaDataError
from metadata.extractor.base import MetaExtractor
from metadata.converter.hive import HiveTypeConverter


class HiveMetaExtractor(MetaExtractor):
    def __init__(self, reader=None):
        super(HiveMetaExtractor, self).__init__()
        self.reader = reader
        self.Engine = "hive"

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
            logging.info("tracing-sql-execution-HiveMetaExtractor: traceid = %s, sql = %s start_execute",
                         self.query_config["traceid"], sql)
            res = self.reader.execute(sql, self.db_config, self.query_config)
            return res
        except Exception as err:
            logging.exception(
                "tracing-sql-execution-HiveMetaExtractor: traceid = %s, sql = %s execute failed, err = %s",
                self.query_config["traceid"], sql, str(err))
            raise MetaDataError(MetaDataErrors.EXTRACTOR_META_ERROR.value,
                                "fail in answering MetaExtract SQL:" + str(err))

    def _get_col_info_list(self):
        sql = "SELECT * FROM {DBName}.{TableName} limit 0".format(DBName=self.DBName, TableName=self.TableName)
        res = self._get_query_answer(sql)
        col_dbtype_list = res.col_type
        col_name_list = list(res.result[0])
        col_type_list = list(map(HiveTypeConverter().dbtype_to_type, col_dbtype_list))
        logging.info("dpaccess-internal-_get_col_info_list col_dbtype_list is {}".format(col_dbtype_list))
        return col_dbtype_list, col_type_list, col_name_list

    def _get_max_fre(self, ColName=None):
        sql = '''select max(FRE) as maxFre
                    from
                        (select
                            {ColName}, count({ColName}) as FRE
                        from
                            {DBName}.{TableName}
                        group by {ColName}) t
                '''.format(DBName=self.DBName, TableName=self.TableName, ColName=ColName)
        res = self._get_query_answer(sql)
        logging.info("dpaccess-internal-_get_max_fre res is {}".format(res))
        return res.result[1][0]

    def _get_max_min(self, ColName=None):
        sql = "select max({ColName}) as upperbound, min({ColName}) as lowerbound from {DBName}.{TableName}".format(
            DBName=self.DBName, TableName=self.TableName, ColName=ColName)
        res = self._get_query_answer(sql)
        logging.info("dpaccess-internal-_get_max_min res is {}".format(res))
        return res.result[1][0], res.result[1][1]

    def execute_extraction(self, DBName=None, TableName=None):
        """
            Extract and construct the complete metadata
        """
        self.DBName = DBName
        self.TableName = TableName
        self.metadata_dict = {"engine": self.Engine, "database": DBName, "tables": []}
        table_dict = {"tablename": TableName, "columns": {}}
        col_dbtype_list, col_type_list, col_name_list = self._get_col_info_list()
        for i in range(len(col_dbtype_list)):
            db_type = col_dbtype_list[i]
            col_type = col_type_list[i]
            col_name = col_name_list[i]
            column_dict = {"type": db_type}
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
                pass
            table_dict["columns"][col_name] = column_dict
        self.metadata_dict["tables"].append(table_dict)


def gen_meta_for_hive(DBName=None, TableName=None, DBConfig=None):
    logging.info("dpaccess-internal gen_meta_for_hive, db_name={}, table_name={}".format(DBName, TableName))
    try:
        hive_reader = HiveDataAccess()
        meta_extractor = HiveMetaExtractor(hive_reader)
        meta_extractor.set_config(DBConfig)
        meta_extractor.execute_extraction(DBName, TableName)
        return meta_extractor.metadata_dict
    except Exception as err:
        raise MetaDataError(MetaDataErrors.HIVE_META_EXCEPTION.value, "HiveMetaExtractor DBName-%s, TableName-%s, "
                                                                      "err-%s" % (DBName, TableName, str(err)))
