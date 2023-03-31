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
from concurrent.futures import ThreadPoolExecutor
from flask import request, Blueprint
from metadata.extractor.clickhouse import gen_meta_for_clickhouse
from metadata.extractor.hive import gen_meta_for_hive
from metadata.storage.metadata_bean_manager import get_table_info, query_meta, delete_meta
from metadata.updater.metadata_gen import generate_meta_budget, generate_update_meta, set_column_clipping

meta = Blueprint('meta', __name__)
executor = ThreadPoolExecutor(20)


@meta.route('/hello', methods=['GET'])
def hello():
    return "hi, hello"


@meta.route('/status', methods=['POST'])
def query_meta_status():
    """query meta status
        1: meta gen finished
        0: meta deleted
        2: meta is being generated
        -1: meta gen failed

        params: (prefix, db_name, table_name)
    """
    try:
        req_json = request.json
        prefix = req_json["prefix"]
        db_name = req_json["db_name"]
        table_name = req_json["table_name"]
        table_info = get_table_info(prefix, db_name, table_name)
        meta_status = None
        if table_info:
            meta_status = table_info.get("status")
        res = {"status_code": 0, "return_msg": "query successfully", "data": meta_status}
        return res
    except Exception as err:
        logging.exception("dpaccess-internal-query_meta_latest_status Exception: \n%s" % str(err))
        return {"status_code": -1, "return_msg": str(err)}


@meta.route('/generate', methods=['POST'])
def gen_metadata():
    """ Generate metadata and store the metadata into Mysql
        params: (db_config(host, db_name, username, password), table_name, db_type)
    """
    try:
        req_json = request.json
        db_config = req_json['db_config']
        table_name = req_json['table_name']
        db_type = req_json['db_type']
        logging.info("gen_metadata: db_config={}, table_name={}, dp_type={}".format(db_config, table_name, db_type))
        if db_type == "clickhouse" or db_type == "hive":
            if db_config and table_name and db_type:
                param = {'prefix': db_config["host"], 'db_name': db_config["database"], 'table_name': table_name, 'db_type': db_type}
                executor.submit(generate_meta_budget, param, db_config)
            else:
                return {"status_code": -1, "return_msg": "The requested parameter is incorrect!"}
        else:
            return {"status_code": -1, "return_msg": "db_type is not support"}
        res = {"status_code": 0, "return_msg": "Generated successfully"}
        return res
    except Exception as err:
        logging.exception("dpaccess-internal-gen_metadata Exception: \n" + str(err))
        return str(err)


@meta.route('/extract', methods=['POST'])
def extract_metadata():
    """ Only generate metadata and show, used for test
        params: (db_config(host, db_name, username, password), table_name, db_type)
    """
    try:
        req_json = request.json
        db_config = req_json['db_config']
        table_name = req_json['table_name']
        db_type = req_json['db_type']
        logging.info("gen_metadata_test: db_config={}, table_name={}, dp_type={}".format(db_config, table_name, db_type))
        if db_config and table_name:
            if db_type == "clickhouse":
                meta = gen_meta_for_clickhouse(db_config["database"], table_name, db_config)
            elif db_type == "hive":
                meta = gen_meta_for_hive(db_config["database"], table_name, db_config)
            else:
                return {"status_code": -1, "return_msg": "db_type={} is not support".format(db_type)}
        else:
            return {"status_code": -1, "return_msg": "The requested parameter is incorrect!"}
        res = {"status_code": 0, "return_msg": "Extracted successfully", "data": meta}
        return res
    except Exception as err:
        logging.exception("dpaccess-internal-gen_metadata_test Exception: \n" + str(err))
        return {"status_code": -1, "return_msg": str(err)}


@meta.route('/get', methods=['GET'])
def get_metadata():
    """ Get a complete metadata
        params: (prefix, db_name, table_name)
    """
    try:
        req_json = request.json
        prefix = req_json["prefix"]
        db_name = req_json["db_name"]
        table_name = req_json["table_name"]
        logging.info("get_metadata: prefix={}, db_name={}, table_name={}".format(prefix, db_name, table_name))
        data = query_meta(prefix, db_name, table_name)
        res = {"status_code": 0, "return_msg": 'Query succeeded', "data": data}
        return res
    except Exception as err:
        logging.exception("dpaccess-internal-get_metadata Exception: \n%s" % str(err))
        return {"status_code": -1, "return_msg": str(err)}


@meta.route('/update', methods=['PUT'])
def update_metadata():
    """Update a complete metadata
        the params of clickhouse/hive: (db_config, table_name, db_type)
    """
    try:
        req_json = request.json
        db_config = req_json['db_config']
        table_name = req_json['table_name']
        db_type = req_json['db_type']
        if db_type == "clickhouse" or db_type == "hive":
            logging.info("update_metadata: db_config={}, table_name={}, db_type={}".format(db_config, table_name, db_type))
            if db_config and table_name and db_type:
                executor.submit(generate_update_meta, db_config["host"], db_config["database"], table_name, db_type, db_config)
            else:
                return {"status_code": -1, "return_msg": "The requested parameter is incorrect!"}
        else:
            return {"status_code": -1, "return_msg": "db_type is not support"}
        res = {"status_code": 0, "return_msg": "Updated successfully"}
        return res
    except Exception as err:
        logging.exception("dpaccess-internal-gen_metadata Exception: \n" + str(err))
        return str(err)


@meta.route('/delete', methods=['DELETE'])
def delete_metadata():
    """Delete a complete metadata
       params: (prefix, db_name, table_name)
    """
    try:
        req_json = request.json
        prefix = req_json["prefix"]
        db_name = req_json["db_name"]
        table_name = req_json["table_name"]
        logging.info("delete_metadata: prefix={}, db_name={}, table_name={}".format(prefix, db_name, table_name))
        if prefix and db_name and table_name:
            delete_meta(prefix, db_name, table_name)
            return {"status_code": 0, "return_msg": "Deleted successfully"}
        else:
            return {"status_code": -1, "return_msg": "The requested parameter is incorrect!"}
    except Exception as err:
        logging.exception("dpaccess-internal-delete_metadata Exception: \n%s" % str(err))
        return {"status_code": -1, "return_msg": str(err)}


@meta.route('/set_clipping', methods=['PUT'])
def set_clipping():
    """Set clipping info for column
        params: (prefix, db_name, table_name, column_name, clipping_info)
    """
    try:
        req_json = request.json
        prefix = req_json['prefix']
        db_name = req_json['db_name']
        table_name = req_json['table_name']
        column_name = req_json['column_name']
        clipping_info = req_json['clipping_info']
        set_column_clipping(prefix, db_name, table_name, column_name, clipping_info)
        return {"status_code": 0, "return_msg": "set successfully"}
    except Exception as err:
        logging.exception("dpaccess-internal-set_clipping Exception: \n%s" % str(err))
        return {"status_code": -1, "return_msg": str(err)}
