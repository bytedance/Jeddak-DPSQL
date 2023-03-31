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

import functools
import typing
import logging
import numpy as np
from analysis.analysis_center import RuleAnalysisCenter
from exception.enum.analysis_errors_enum import AnalysisErrors
from exception.enum.privacyaccountant_errors_enum import PrivacyAccountantErrors
from exception.enum.queryinterface_errors_enum import QueryInterfaceErrors
from query_driver.context import Context
from analysis.pre_analysis_center import PreAnalysisCenter, NoiseSwitch
from analysis.analysis_info import is_contain_aggfunc, is_contain_join
from dbaccess.dbaccess import DbAccess
from dbaccess.queryresult import QueryResult
from exception.errors import QueryInterfaceError, PrivacyAccountantError, AnalysisError
from metadata.matcher.matcher_factory import get_metamatcher
from differential_privacy.noise.elasticsensitivity import ElasticSensitivity
from parser.utils import ast_utils, ast_converter
from parser.symbol.ast_symbols_loader import load_ast_symbols
from parser.ast.type.node_type import DialectType, NodeType
from differential_privacy.rewriter.rewrite_based import RewriteBasedRewriter
from differential_privacy.rewriter.result_based import ResultBasedRewriter
from differential_privacy.rewriter.rewrite_noise import noise_addition_rewriter
from differential_privacy.accountant.noise import laplace_float, laplace_int, normal_int, normal_float
from differential_privacy.accountant.accountant import PrivDataGroup, record_budget_info, is_budget_depleted
from differential_privacy.accountant.utility import get_utility_dict
from utils.time_perf import TimePerf, EmptyTimePerf
from differential_privacy.noise.sensitivity import CalSensitivity
from differential_privacy.accountant.init_config import init_dpconfig
import threading


QUERYINTERFACE = "queryinterface"


class DPSQLResult:
    def __init__(self, query_result: QueryResult, context: Context):
        self.query_result = query_result
        self.context = context

    def get_query_result(self):
        return self.query_result

    def get_debug_info(self):
        return self.context.construct_debug_info()

    def get_dp_info(self):
        return self.context.construct_dp_info()


class DPSQL:
    """
    The entry class, provide query interface, and unified organization of the underlying modules to work together.

     Raises:
         QueryInterfaceError: Identify the module where the exception occurred
    """
    NAME = 0
    SYMBOL = 1
    # The maximum number of retries allowed for result-based noise addition
    MAX_RETRY_TIMES = 10

    def __init__(self):
        # init context
        self.context = Context()
        self.ruleAnalysis = RuleAnalysisCenter()
        self._init_context_dpconfig()

    def _init_context_dpconfig(self):
        dpconfig = init_dpconfig()
        method = dpconfig.get("dp_method")
        budget_setting = dpconfig.get("budget_setting")
        self.context.set_context("dpconfig", dpconfig)
        self.context.set_context("method", method)
        self.context.set_context('budget_setting', budget_setting)

    def execute(self, sql: str, dbconfig: dict,
                queryconfig: dict) -> DPSQLResult:
        """Get DPSQLResult object for execute result.

        Execute sql and get the result, record runtime param and format result with DPSQLResult

        Args:
            sql: target sql.
            dbconfig: Param for access database
            queryconfig: Optional param for execute sql

        Returns:
            DPSQLResult object contains QueryResult and Context.

        Raises:
            QueryInterfaceError: An error occurred QueryInterface module process.
        """
        try:
            extra = self.context.get_context("extra")
            if extra is not None:
                debug = extra.get('debug')
            else:
                debug = False
            # init time perf
            time_perf = TimePerf() if debug else EmptyTimePerf()
            self.context.set_context("time_perf", time_perf)
            # get the start timestamp of query_interface
            time_perf.time_start("query_interface")
            # Record raw sql
            self.context.set_context("source_sql", sql)
            # create dbaccess
            dbaccess = DbAccess(dbconfig)
            self.context.set_context("dbaccess", dbaccess)
            # Currently no matching reader
            if dbaccess.get_reader() is None:
                logging.warning("dpaccess-internal-current reader type not match")
                raise QueryInterfaceError(QueryInterfaceErrors.REDERTYPE.value, "reader type not match")
            # get the start timestamp of parser
            time_perf.time_start("parser")
            traceid = self.context.get_context("trace_id")
            # Get the parsed ast
            reader_info = dbconfig.get("reader").lower()
            ast = ast_converter.get_ast(sql, reader_info)
            self.context.set_context("ast", ast)
            # generate meta matcher
            meta_matcher = get_metamatcher(sql, dbconfig, traceid)
            self.context.set_context("meta_matcher", meta_matcher)
            # record the end timestamp of parser
            time_perf.time_end("parser")
            # record the start timestamp of analysis
            time_perf.time_start("analysis")
            rule_engines = self.ruleAnalysis.get_rule_engines()
            for rule_engine in rule_engines:
                rule_engine.excute(ast)
            self.context.set_context("dbconfig", dbconfig)
            # pre analysis sql ast
            pac = PreAnalysisCenter()
            self._analysis_basic_info(pac)
            noise_switch_info = self.context.get_context("noise_switch_info")

            table_list = self.context.get_context("table_list")
            # record the end timestamp of analysis
            time_perf.time_end("analysis")
            # attach privacy accountant to specified tables in sql
            privdatas = PrivDataGroup()
            privdatas.init(table_list, dbconfig)
            if is_budget_depleted(privdatas):
                raise ValueError("Sorry, the budget of corresponding table is exhausted, and the sql is rejected.")
            self.context.set_context("privdatas", privdatas)
            # dispatch
            parsed_sql = ast
            self.context.set_context("parsed_sql", parsed_sql)
            query_result = None
            if noise_switch_info == NoiseSwitch.NOT_NOISE:
                logging.warning("pre analysis-NOT_NOISE: " + sql)
                raise QueryInterfaceError(QueryInterfaceErrors.ADD_NOISE_ERROR.value, "The input Sql is not supported, sensitivity can not be calculate")
            elif noise_switch_info == NoiseSwitch.NOISE_REWRITE_PROCESS:
                self.context.set_context("noise_method", "rewrite add noise")
                load_ast_symbols(ast, meta_matcher)
                logging.info("tracing-sql-execution-executor-" + traceid + ":" + "use rewrite based processing")
                raise QueryInterfaceError(QueryInterfaceErrors.ADD_NOISE_ERROR.value, "Rewrite based processing is not ready")
            elif noise_switch_info == NoiseSwitch.NOISE_POST_PROCESS:
                self.context.set_context("noise_method", "result-based add noise")
                load_ast_symbols(ast, meta_matcher)
                logging.info("tracing-sql-execution-executor-" + str(traceid) + ":" + "use result-based processing")
                query_result = self._result_based_noise(dbconfig, queryconfig)
            else:
                raise AnalysisError(AnalysisErrors.NOISE_SWITCH_ERROR.value,
                                    "Internal error: unknown noise switch: " + str(noise_switch_info))
            # get the end timestamp of query_interface
            time_perf.time_end("query_interface")
            return query_result
        except Exception as err:
            raise QueryInterfaceError(QueryInterfaceErrors.QUERYINTERFACE_EXCEPTION.value, err)

    # via pre-analysis center get basic info
    def _analysis_basic_info(self, pac):
        ast = self.context.get_context("ast")
        basic_meta_info = pac.getBasicMetaInfo(ast)
        struct_info = pac.getStructInfo(ast)
        noise_switch_info = pac.getNoiseSwitch(ast)
        self.context.set_context("noise_switch_info", noise_switch_info)
        self.context.set_context("basic_info", basic_meta_info)
        self.context.set_context("struct_info", struct_info)
        dbconfig = self.context.get_context("dbconfig")
        if dbconfig.get("database") is None:
            dbconfig["database"] = basic_meta_info.database
        table_list = basic_meta_info.table
        # Deduplication
        table_list = list(set(table_list))
        self.context.set_context("table_list", table_list)

    # Noise based on rewriting
    def _rewrite_based_noise(self, dbconfig: dict, queryconfig: dict) -> QueryResult:
        dbaccess = self.context.get_context("dbaccess")
        method = self.context.get_context("method")
        logging.info("add rewriter noise method: ", str(method))
        parsed_sql = self.context.get_context("parsed_sql")
        meta = self.context.get_context("meta_matcher")
        rewriter = RewriteBasedRewriter(parsed_sql)
        rewriter.rewrite()
        load_ast_symbols(parsed_sql, meta)
        traceid = self.context.get_context("trace_id")
        logging.info("add rewriter noise trace id: ", str(traceid))
        time_perf = self.context.get_context("time_perf")
        # get the start timestamp of rewriter
        time_perf.time_start("rewriter")
        struct_info = self.context.get_context("struct_info")
        # overwrite noise
        privdatas = self.context.get_context("privdatas")
        noise_addition_rewriter(parsed_sql, privdatas, struct_info)
        rewrite_sql = ast_utils.tosql(parsed_sql, DialectType.CLICKHOUSE)
        time_perf.time_end("rewriter")
        # get the start timestamp of query_execute
        time_perf.time_start("query_execute")
        extra = self.context.get_context("extra")
        result = dbaccess.execute(rewrite_sql, dbconfig, queryconfig, extra)
        time_perf.time_end("query_execute")
        return DPSQLResult(result, self.context)

    # Noise based on results
    def _result_based_noise(self, dbconfig: dict, queryconfig: dict) -> QueryResult:
        """
        Using result based method to process query, return the query result. Result based
        means adding noise on the result data returned by database.
        Parameters:
            dbconfig: Param for access database
            queryconfig: Optional param for execute sql
        Returns:
            QueryResult
                The differential privacy protected sql query result.
        """
        traceid = self.context.get_context("trace_id")
        time_perf = self.context.get_context("time_perf")
        time_perf.time_start("rewriter")
        parsed_sql = self.context.get_context("parsed_sql")
        method = self.context.get_context("method")
        rewriter = ResultBasedRewriter(parsed_sql)
        rewritten_sql = rewriter.rewrite().get_result()
        meta = self.context.get_context("meta_matcher")
        load_ast_symbols(rewritten_sql, meta)
        rewriter.fix()
        subquery = rewritten_sql.source_block.source.select_query
        self.context.set_context("rewrited_sql", str(rewritten_sql))
        #
        # get the end timestamp of rewriter
        time_perf.time_end("rewriter")
        # WARNING: Code should not rely on private function of reader, this part will be deprecated
        logging.info("tracing-sql-execution-rewriter-postmethod-" + str(traceid) + "-" + "subquery:" + str(subquery))
        # get the start timestamp of query_execute
        time_perf.time_start("query_execute")
        dbaccess = self.context.get_context("dbaccess")
        extra = self.context.get_context("extra")
        subquery_result = dbaccess.execute_ast(subquery, dbconfig, queryconfig, extra=extra)
        logging.info("tracing-sql-execution-rewriter-postmethod-" + str(traceid) + "-" + "subquery result:" + str(subquery_result))
        # get the end timestamp of query_execute
        time_perf.time_end("query_execute")
        subquery_data = subquery_result.get_result()
        # get each symbol for sensitivity analysis
        data_symbols = subquery.select_statements[0].select_block.m_symbols
        source_col_names = tuple(s[DPSQL.NAME] for s in data_symbols)
        logging.info("dpaccess-internal-" + str(source_col_names))
        # get the start timestamp of sensitivity analysis
        time_perf.time_start("sensitivity_analysis")
        min_val, agg = self._get_postprocessing_info(data_symbols)
        struct_info = self.context.get_context("struct_info")
        privdatas = self.context.get_context("privdatas")
        # get sensitivity list
        if is_contain_join(struct_info) is False:
            sensitivities = tuple(sym[self.SYMBOL].sensitivity() for sym in data_symbols)
        else:
            sensitivities = self._get_elastic_sensitivity(rewritten_sql, privdatas)
        self.context.set_context("source_col_names", source_col_names)
        self.context.set_context("sensitivities", sensitivities)
        logging.info("tracing-sql-execution-rewriter-postmethod-" + str(traceid) + "-" + "sensitivities:" + str(sensitivities))
        # However group keys are not considered for properties such as sensitivities
        is_grouping_keys = DPSQL._get_grouping_keys(subquery=rewritten_sql, symbols=source_col_names)
        # Delete grouping keys from sensitivity symbols
        sensitivities = tuple(map(lambda x, y: None if x else y,
                                  is_grouping_keys, sensitivities))

        # get the end timestamp of sensitivity analysis
        time_perf.time_end("sensitivity_analysis")
        # get the start timestamp of post_processing
        time_perf.time_start("post_processing")
        # allocate privacy cost for columns and estimate the utility of dp result
        epsilons, delts = self._allocate_privacy(sensitivities)
        if method.lower() in ["gauss"]:
            sensitivities = CalSensitivity.cal_ord_norm_sensitivity(sensitivities, ord=2)
            epsilons = np.array(epsilons)
            epsilons[epsilons > 0] = np.sum(epsilons)
            delts = np.array(delts)
            delts[delts > 0] = np.sum(delts)
        privdatas = self.context.get_context("privdatas")
        out_col_names = tuple(str(s[DPSQL.NAME]) for s in rewritten_sql.select_block.m_symbols)
        # Adding noise to each result of subquery
        noise_data = map(
            functools.partial(DPSQL._add_noise, sensitivities=sensitivities, privdatas=privdatas, epsilons=epsilons,
                              delts=delts,
                              traceid=traceid, min_val=min_val, agg=agg, method=method),
            subquery_data[1:]
        )
        noise_data_list = list(noise_data)
        utility_dict_list = []
        if method.lower() in ["laplace"]:
            utility_dict_list = list(map(functools.partial(
                get_utility_dict,
                epsilons=epsilons,
                sensitivities=sensitivities,
                source_col_names=source_col_names,
                rewritten_sql=rewritten_sql,
            ), noise_data_list))
        self.context.set_context("utility_dict_list", utility_dict_list)
        # Now reunion the final result
        query_result = QueryResult()
        noise_data = map(functools.partial(
            DPSQL._post_process_result,
            source_col_names=source_col_names,
            rewritten_sql=rewritten_sql
        ), noise_data_list)
        query_result.set_result([tuple(out_col_names)] + list(noise_data))
        # reunion the column datatype
        out_types = list(
            s[DPSQL.SYMBOL].dbtype(meta.type_converter) for s in rewritten_sql.select_block.m_symbols)
        # prefer to use database returned col type
        subquery_res_meta = subquery_result.get_meta()
        logging.debug(subquery_res_meta)
        for i in range(len(out_col_names)):
            orig_type = subquery_res_meta.get(out_col_names[i], None)
            if orig_type is not None:
                out_types[i] = orig_type
        logging.debug(out_types)
        query_result.set_type(tuple(out_types))
        logging.info("tracing-sql-execution-rewriter-postmethod-" + str(traceid) + "-" + "noised result:" + str(query_result))
        # get the end timestamp of post_processing
        time_perf.time_end("post_processing")
        try:
            record_budget_info_task = threading.Thread(target=record_budget_info, args=(privdatas,))
            record_budget_info_task.start()
        except Exception as err:
            logging.exception("tracing-sql-execution-privacy-accountant" + traceid + "-" + str(err))
            raise PrivacyAccountantError(PrivacyAccountantErrors.ADD_ERROR.value, err)
        finally:
            return DPSQLResult(query_result, self.context)
        return DPSQLResult(query_result, self.context)

    # get agg type and min val for post processing
    def _get_postprocessing_info(self, data_symbols):
        min_val = []
        agg = []
        # # Get the aggregation operation type and metadata
        for sym in data_symbols:
            ident_flag = ast_utils.is_node(sym[self.SYMBOL], NodeType.Identifier_EXPR)
            if ident_flag is True:
                sym = sym[self.SYMBOL].symbol
            else:
                sym = sym[self.SYMBOL]
            agg_flag = ast_utils.is_node(sym, NodeType.SqlAggFunction_EXPR)
            if agg_flag is True:
                agg.append(sym.func_name.lower())
                min_val.append(None)
            else:
                agg.append(None)
                min_val.append(None)
        return min_val, agg

    # allocate privacy via sensitivity
    def _allocate_privacy(self, sensitivities):
        budget_setting = self.context.get_context('budget_setting')
        set_epsilon = budget_setting.get("epsilon")
        set_delt = budget_setting.get("delt")
        epsilons = []
        delts = []
        method = self.context.get_context("method")
        privdatas = self.context.get_context("privdatas")
        struct_info = self.context.get_context("struct_info")
        for sens in sensitivities:
            if sens is not None and is_contain_join(
                    struct_info) is False and method.lower() == "gauss":
                # TODO: lack of a reasonable way to allocate privacy cost for columns
                eps, delt_val = privdatas.allocate_cost_gauss(set_epsilon, set_delt)
                epsilons.append(eps)
                delts.append(delt_val)
            elif sens is not None and is_contain_join(struct_info) is False:
                eps, delt_val = privdatas.allocate_cost(set_epsilon)
                epsilons.append(eps)
                delts.append(delt_val)
            elif sens is not None and is_contain_join(struct_info) is True:
                eps, delt_val = privdatas.allocate_cost_for_join(set_epsilon, set_delt)
                epsilons.append(eps)
                delts.append(delt_val)
            else:
                epsilons.append(0)
                delts.append(0)
        return epsilons, delts

    # For the purpose of encapsulation, function used only in class should be defined as static private
    @staticmethod
    def _get_grouping_keys(subquery,
                           symbols: typing.List[str]) -> typing.List[bool]:
        """
        Getting the grouping keys of the subquery if any.

        Parameters:
            subquery: ast.AST
                The rewritten subquery for each subquery
        Returns:
            A list of bool indicates the corresponding sensitivity is a grouping key or not.
        """
        group_keys = tuple()
        m_symbols = subquery.select_block.m_symbols
        if is_contain_aggfunc(m_symbols):
            group_keys = tuple(
                ge[DPSQL.NAME]
                for ge in m_symbols
                if hasattr(ge[DPSQL.SYMBOL], "is_group_key") and ge[DPSQL.SYMBOL].is_group_key is True
            )
        return tuple(col in group_keys for col in symbols)

    @staticmethod
    def _add_noise(row_in, sensitivities: typing.Iterable, privdatas: PrivDataGroup, epsilons: typing.Iterable,
                   delts: typing.Iterable, traceid, min_val, agg, method) -> typing.Tuple[float]:
        # Pull out tuple values
        row = [v for v in row_in]
        # Set null to 0 before adding noise
        for idx, sen in zip(range(len(row)), sensitivities):
            if sen is not None and row[idx] is None:
                row[idx] = 0.0
        # Call all mechanisms to add noise
        out_row = list()
        # Record the amount of noise needed and the number of failures
        add_noise_total = 0
        add_noise_err = 0
        # Record the current column index
        index = 0
        for s, eps, delt, v in zip(sensitivities, epsilons, delts, row):
            # Flag bit, to determine whether to add noise again
            retry_tag = True
            # record raw value
            source = v
            # "" empty string is used to represent null
            # TODO: handle more elegant way
            if type(v) == str:
                out_row.append(v)
                index = index + 1
                continue
            if s is None:
                out_row.append(v)
            else:
                add_noise_total = add_noise_total + 1
                # Record the current number of retries
                current_retry_time = 0
                while current_retry_time < DPSQL().MAX_RETRY_TIMES and retry_tag is True:
                    current_retry_time = current_retry_time + 1
                    if type(v) is int:
                        if method.lower() == "laplace":
                            noise = laplace_int(s, eps)
                        else:
                            noise = normal_int(s, eps, delt)
                    elif type(v) is float:
                        if method.lower() == "laplace":
                            noise = laplace_float(s, eps)
                        else:
                            noise = normal_float(s, eps, delt)
                    else:
                        raise QueryInterfaceError(QueryInterfaceErrors.ADD_NOISE_ERROR.value,
                                                  "Adding noise: don not know how to handle " + str(type(v)))
                    v = source + noise
                    # Determine whether the current operation is of count type
                    if agg[index] == "count":
                        # non-negative-legal
                        if v >= 0:
                            retry_tag = False
                        else:
                            v = source
                    # Determine whether the current operation is sum, and there is a minimum value in the metadata
                    elif agg[index] == "sum" and min_val[index] is not None:
                        # The result of adding noise is not less than the current minimum value
                        if v >= min_val[index]:
                            retry_tag = False
                        else:
                            v = source
                index = index + 1
                # add the privacy cost of this call to dp
                if method.lower() == "laplace":
                    privdatas.incrby(eps)
                # 判断在重试次数内是否有符合要求值，若无使用原值兜底
                if retry_tag is True and v <= 0:
                    v = source
                    add_noise_err = add_noise_err + 1
                out_row.append(v)
        if method.lower() == "gauss":
            privdatas.incrby(epsilons[0], delts[0])
        return tuple(out_row)

    @staticmethod
    def _convert(val: typing.Union[str, int, bool, float], val_type: str) -> typing.Union[str, int, bool, float]:
        if val_type == "string" or val_type == "unknown":
            return str(val).replace('"', "").replace("'", "")
        elif val_type == "int":
            if val is None or val == "":
                return ""
                # raise Exception("excute result is null:", val)
            return int(float(str(val).replace('"', "").replace("'", "")))
        elif val_type == "float":
            if val is None or val == "":
                return ""
                # raise Exception("excute result is null:", val)
            return float(str(val).replace('"', "").replace("'", ""))
        elif val_type == "boolean":
            if isinstance(val, int):
                return val != 0
            else:
                if val is None:
                    raise QueryInterfaceError(QueryInterfaceErrors.RESULT_NULL.value, f"excute result is null: {val}")
                return bool(str(val).replace('"', "").replace("'", ""))
        else:
            raise QueryInterfaceError(QueryInterfaceErrors.CONVERT_TYPE_ERROR.value, f"Can't convert type: {val_type}")

    @staticmethod
    def _post_process_result(row, rewritten_sql,
                             source_col_names: typing.List[str]):
        bindings = dict((name.lower(), val) for name, val in zip(source_col_names, row))
        row = tuple(c.expr.evaluate(bindings) for c in rewritten_sql.select_block.nameExpressions)
        return row

    def _get_elastic_sensitivity(self, ast, privdatas):
        sensitivity = []
        elastic_sensitivity = ElasticSensitivity()
        struct_info = self.context.get_context("struct_info")
        ji_list = struct_info.struct_join_info.join_infos
        for item in ast.select_block.m_symbols:
            agg_flag = ast_utils.is_node(item[self.SYMBOL], NodeType.SqlAggFunction_EXPR)
            if agg_flag is False:
                sensitivity.append(None)
            else:
                epsilon, delta = privdatas.allocate_cost_for_join()
                # 2.2 Calculate smoothing sensitivity
                smooth_sensitivity = elastic_sensitivity.smooth_elastic_sensitivity(ji_list, epsilon, delta)
                agg_sum_flag = ast_utils.is_node(item[self.SYMBOL], NodeType.SqlSumFunction_EXPR)
                if agg_sum_flag is True:
                    max_val = item[self.SYMBOL].args._list[0].symbol.maxval
                    min_val = item[self.SYMBOL].args._list[0].symbol.minval
                    var = abs(max_val - min_val)
                    sensitivity.append(2 * var * smooth_sensitivity)
                else:
                    sensitivity.append(2 * smooth_sensitivity)
        return tuple(sensitivity)
