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

import json
import logging
from exception.enum.httpservice_errors_enum import HttpServiceErrors
from exception.errors import UtilsError
from http_service.api.protocol_common import construct_error_json, convert_result_tojson
from query_driver.dpsql import DPSQL
from utils.traceid import trace_id_standard
from differential_privacy.accountant.init_config import init_dpconfig


def dpsql_http_interface_query(request):
    try:
        # read proto
        # Track related by traceid with log
        req_json = request.json
        sql = req_json['sql']
        dbconfig = req_json['dbconfig']
        queryconfig = req_json['queryconfig']
        traceid = queryconfig.get('traceid')
        dpconfig = req_json.get('dpconfig')
        extra = req_json.get('extra')
        # Obtain and generate trace id and manage it uniformly
        traceid, queryconfig, dbconfig = trace_id_standard(traceid, queryconfig, dbconfig)
        # The debug switch is turned off by default
        debug = False
        dpconfig = init_dpconfig(dpconfig)
        method = dpconfig.get("dp_method")
        budget_setting = dpconfig.get("budget_setting")
        if method.lower() not in ["", None, "laplace", "gauss"]:
            raise UtilsError(HttpServiceErrors.ALG_PARAM_ERROR.value, "param dp method Error")
        if extra is not None:
            debug = extra.get('debug')
        logging.info("tracing-sql-execution-sqlparam-interface-%s:%s" % (traceid, sql))
        logging.info("tracing-sql-execution-request-interface-%s:%s" % (traceid, json.dumps(req_json)))
        # create dpsql object
        dpsql_instance = DPSQL()
        # context记录dpconfig信息
        dpsql_instance.context.set_context("dpconfig", dpconfig)
        dpsql_instance.context.set_context("method", method)
        dpsql_instance.context.set_context('budget_setting', budget_setting)
        # context record extra信息
        dpsql_instance.context.set_context("extra", extra)
        dpsql_instance.context.set_context("trace_id", traceid)
        # do query
        res = dpsql_instance.execute(sql, dbconfig, queryconfig)
        logging.info("dpaccess-internal-col-interface type is: \n %s" % str(res.get_query_result().get_type()))
        # convert to json proto
        res_format = convert_result_tojson(res, debug)
        logging.info(
            "tracing-sql-execution-response-interface-%s:%s-request-%s" % (traceid, res_format, json.dumps(req_json)))
    except Exception as err:
        logging.exception("tracing-sql-execution-interface-exception-%s-Exception: %s-request-%s" % (
            traceid, str(err), json.dumps(req_json)))
        res_format = construct_error_json(1, str(err))
    return res_format
