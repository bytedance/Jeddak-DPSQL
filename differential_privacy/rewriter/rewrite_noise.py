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

from analysis.analysis_info import is_contain_join
from differential_privacy.accountant.accountant import PrivDataGroup
from exception.enum.rewriter_errors_enum import RewriterErrors
from exception.errors import RewriterError
from differential_privacy.noise.elasticsensitivity import ElasticSensitivity
import parser.ast.expr.base_expr as nt
from parser.utils import ast_utils
from parser.ast.expr.agg_function_expr import SqlCountFunction, SqlSumFunction, SqlMaxFunction, SqlMinFunction
from parser.ast.expr.arithmetic_expr import AdditionExpression
from parser.ast.expr.other import CastExpr
from parser.ast.type.node_type import NodeType
from analysis.feature_analysis_visitor import ComplexSqlAnalysis
import logging


# def laplaceSample(sens, eps, round_tag):
#     scale = sens / eps
#     # random value: rand64()%100000/110000-0.49
#     rand_func = BareFunction(FuncName("rand64"))
#     rand_value = ArithmeticExpression(rand_func, '%', Literal(100000.0))
#     rand_value = ArithmeticExpression(rand_value, '/', Literal(110000.0))
#     rand_value = ArithmeticExpression(rand_value, '-', Literal(0.49))
#
#     # sign: (case when rand64()%100000/110000-0.49>0 then 1.0 else -1.0 end)
#     cmp0 = BooleanCompare(rand_value, Op('>'), Literal(0))
#     when_expr = WhenExpression(cmp0, Literal(1.0))
#     sign = CaseExpression(None, [when_expr, ], Literal(-1.0))
#
#     # abs(rand64()%100000/110000-0.49)
#     abs_func = MathFunction(FuncName("abs"), rand_value)
#
#     # 1-2*abs(rand64()%100000/110000-0.49)
#     ln_arg = ArithmeticExpression(Literal(2), Op('*'), abs_func)
#     ln_arg = ArithmeticExpression(Literal(1), Op('-'), ln_arg)
#
#     # ln func
#     ln_fun = CommonFunction(FuncName("ln"), [ln_arg, ], None)
#
#     # scale * sign * ln func
#     lap_sample = ArithmeticExpression(sign, Op('*'), ln_fun)
#     lap_sample = ArithmeticExpression(Literal(scale), Op('*'), lap_sample)
#     # 判断是否需要取整处理
#     if round_tag is True:
#         # TODO:仅针对clickhouse进行处理，如何实现更通用的方式
#         lap_sample = MathFunction(FuncName("toInt32"), lap_sample)
#     return NestedExpression(lap_sample)
#
#
# def laplaceNoiseRewriter(expr, sens, eps, round_tag):
#     return NestedExpression(ArithmeticExpression(expr, Op('+'), laplaceSample(sens, eps, round_tag)))


def noise_addition_rewriter(sql_ast, privdatas: PrivDataGroup, struct_info):
    csa = ComplexSqlAnalysis(sql_ast)
    flag, msg = csa.isNeedRewriteNoise()
    if flag is False:
        logging.debug("不可以执行重写加噪 ： " + msg)
        raise RewriterError(RewriterErrors.REWRITER_ADD_NOISE_ERROR.value, "不可以执行重写加噪-" + msg)
    agg_nodes = csa.get_all_agg_nodes()
    for node in agg_nodes:
        noise_expr = _build_noise_expr_node_for_agg(node, privdatas, struct_info)
        ast_utils.replaceAstNode(node, noise_expr)


def noise_addition_rewriter_sq(sq, analysis_result, privdatas: PrivDataGroup, struct_info):
    agg_list = analysis_result.rewrite_agg_list
    for node in agg_list:
        noise_expr = _build_noise_expr_node_for_agg_sq(node, sq, privdatas, analysis_result.struct_info)
        ast_utils.replaceAstNode(node, noise_expr)


def _build_noise_expr_node_for_agg_sq(agg_node, sq, privdatas: PrivDataGroup, struct_info):
    # 判断是否包含聚合操作
    is_join = None
    if len(struct_info.struct_join_info.join_infos) == 0:
        is_join = False
    else:
        is_join = True
    ne = nt.NestedExpression()
    # 隐私消耗
    epsilon, delta = _privas_allocate(privdatas, is_join)
    sensitivity = _calculate_node_sensitivity_sq(agg_node, struct_info, is_join, epsilon, delta)
    scale = sensitivity / epsilon
    # 噪声计算表达式
    cal_noise = str(
        scale) + " *  (case when rand64()%100000/110000-0.49>0 then 1.0 else -1.0 end) * ln(1-2*abs(rand64()%100000/110000-0.49))"
    noise_expr = ast_utils.createExprNode(cal_noise)
    ae = AdditionExpression(agg_node.clone(), noise_expr)
    ae_expr_str = str(ae)
    ae = _filter_for_agg_node(agg_node, ae_expr_str, sensitivity)
    ne.expr = ae

    return ne


def _build_noise_expr_node_for_agg(agg_node, privdatas: PrivDataGroup, struct_info):
    # 是否包含join操作
    is_join = is_contain_join(struct_info)
    ne = nt.NestedExpression()
    # 隐私消耗
    epsilon, delta = _privas_allocate(privdatas, is_join)
    # 敏感度计算
    sensitivity = _calculate_node_sensitivity(agg_node, is_join, epsilon, delta, struct_info)
    scale = sensitivity / epsilon
    # 噪声计算表达式
    cal_noise = str(
        scale) + " *  (case when rand64()%100000/110000-0.49>0 then 1.0 else -1.0 end) * ln(1-2*abs(rand64()%100000/110000-0.49))"
    noise_expr = ast_utils.createExprNode(cal_noise)
    ae = AdditionExpression(agg_node.clone(), noise_expr)
    ae_expr_str = str(ae)
    ae = _filter_for_agg_node(agg_node, ae_expr_str, sensitivity)
    ne.expr = ae

    return ne


# 过滤选择器
def _filter_for_agg_node(agg_node, ae_expr_str, max_val):
    # TODO: 使用metadata获取最值
    min_val = 0
    # count类型非法值过滤表达式生成
    if type(agg_node) is SqlCountFunction:
        ae_expr_str = _build_filter_node_for_count(ae_expr_str)
    # sum类型非法值过滤表达式生成
    if type(agg_node) is SqlSumFunction:
        ae_expr_str = _build_filter_node_for_sum(ae_expr_str, min_val)
    # max类型非法值过滤表达式生成
    if type(agg_node) is SqlMaxFunction:
        ae_expr_str = _build_filter_node_for_max(ae_expr_str, max_val)
    # min类型非法值过滤表达式生成
    if type(agg_node) is SqlMinFunction:
        ae_expr_str = _build_filter_node_for_min(ae_expr_str, min_val)
    # 聚合函数里第一层有无cast类型需要处理
    if hasattr(agg_node, "args") and len(agg_node.args._list) > 0:
        cur = agg_node.args._list[0]
        if type(cur) is CastExpr:
            dest_type = str(cur.dest_type_expr)
            ae_expr_str = _build_cast_node(ae_expr_str, dest_type)
    ae = ast_utils.createExprNode(ae_expr_str)
    return ae


# 保证聚合函数里有cast函数时加噪后数值类型一致
def _build_cast_node(ae_expr_str, cast_type):
    ce_expr_str = "CAST( " + ae_expr_str + ", '" + cast_type + "' )"
    return ce_expr_str


# # 获取当前聚合操作col的meta
# def analysis_col_meta_extreme(agg_node):
#     curent_info = agg_node.args._list[0]
#     # map类型
#     if hasattr(curent_info, "map_info"):
#         max_val = curent_info.map_info.maxval
#         min_val = curent_info.map_info.minval
#     else:
#         max_val = curent_info.symbol.maxval
#         min_val = curent_info.symbol.minval
#     return max_val, min_val


# 测试方法
def _calculate_node_sensitivity_sq(agg_node, struct_info, is_join, epsilon, delta=None):
    if is_join is True:
        elastic_sensitivity = ElasticSensitivity()
        ji_list = struct_info.struct_join_info.join_infos
        smooth_sensitivity = elastic_sensitivity.smooth_elastic_sensitivity(ji_list, epsilon, delta)
        # count类型计算方式
        if type(agg_node) is SqlCountFunction:
            sensitivity = 2 * smooth_sensitivity
        # sum类型计算方式
        elif type(agg_node) is SqlSumFunction:
            max_val, min_val = elastic_sensitivity, 0
            var = abs(max_val - min_val)
            sensitivity = 2 * var * smooth_sensitivity
    else:
        sensitivity = agg_node.sensitivity()
    return sensitivity


# 计算当前节点敏感度
def _calculate_node_sensitivity(agg_node, is_join, epsilon, delta, struct_info):
    # 含有join且join表为物理表
    if is_join is True and _is_SqlTableSource_join(struct_info) is True:
        elastic_sensitivity = ElasticSensitivity()
        ji_list = struct_info.struct_join_info.join_infos
        smooth_sensitivity = elastic_sensitivity.smooth_elastic_sensitivity(ji_list, epsilon, delta)
        # count类型计算方式
        if type(agg_node) is SqlCountFunction:
            sensitivity = 2 * smooth_sensitivity
        # sum类型计算方式
        elif type(agg_node) is SqlSumFunction:
            max_val, min_val = elastic_sensitivity, 0
            var = abs(max_val - min_val)
            sensitivity = 2 * var * smooth_sensitivity
        # 其他聚合类型按一般敏感度计算
        else:
            sensitivity = agg_node.sensitivity()
    # 不含join
    else:
        sensitivity = agg_node.sensitivity()
    return sensitivity


# 分配隐私消耗
def _privas_allocate(privdatas: PrivDataGroup, is_join):
    if is_join is True:
        epsilon, delta = privdatas.allocate_cost_for_join()
    else:
        epsilon, delta = privdatas.allocate_cost()
    return epsilon, delta


# count类型非法值过滤
def _build_filter_node_for_count(ae_expr_str):
    # round取整
    round_expr = "toUInt64( round( " + ae_expr_str + " ) )"
    # 加入if条件判断,防止负数和除0现象
    if_expr = "if( " + round_expr + " < 1 , 1, " + round_expr + " )"
    return if_expr


# sum类型非法值过滤
def _build_filter_node_for_sum(ae_expr_str, min_val):
    if_expr = "if( " + ae_expr_str + " < " + str(min_val) + " , " + str(min_val) + " , " + ae_expr_str + " )"
    return if_expr


# max类型非法值过滤
def _build_filter_node_for_max(ae_expr_str, max_val):
    if_expr = "if( " + ae_expr_str + " < " + str(max_val) + " , " + str(max_val) + " , " + ae_expr_str + " )"
    return if_expr


# min类型非法值过滤
def _build_filter_node_for_min(ae_expr_str, min_val):
    if_expr = "multiIf( " + ae_expr_str + " < 0, " + str(min_val) + " , " + ae_expr_str + " > " + str(
        min_val) + " , " + str(min_val) + " , " + ae_expr_str + " )"
    return if_expr


# 检查join表是否均为物理表
def _is_SqlTableSource_join(struct_info):
    ji_list = struct_info.struct_join_info.join_infos
    for item in ji_list:
        if item.table1_type is not NodeType.SqlTableSource or item.table2_type is not NodeType.SqlTableSource:
            return False
    return True

# def noise_addition_rewriter(parsed_sql, privdatas):
#     # find AggFunction(TableColumn|MapExpression)
#     select_expr = parsed_sql.select
#     aggF_list = []
#     logging.debug(parsed_sql)
#     for ne in select_expr.namedExpressions:
#         expr = ne.expression
#         aggfuns = expr.find_nodes(AggFunction)
#         if type(expr) is AggFunction:
#             aggfuns.append(expr)
#         # logging.debug(ne.m_symbol)
#         for aggf in aggfuns:
#             # if TableColumn MapExpression is directly from relation
#             if len(aggf.sym.find_nodes(AggFunction)):
#                 continue
#             logging.debug(aggf.sym)
#             # 获取table column符号对象
#             table_column = aggf.sym.find_nodes(TableColumn)
#             # 获取map表达式符号对象
#             map_exp = aggf.sym.find_nodes(MapExpression)
#             # map表达需要dp加噪需要取整类型
#             standard = ["int", "int64", "int32"]
#             # round_tag标记是否需要取整
#             round_tag = False
#             # 针对count做判断
#             if aggf.is_count is False and len(table_column) == 0 and len(map_exp) == 0:
#                 continue
#             # 对于col为int类型或count操作加噪需要取整
#             if aggf.is_count is True or (len(table_column) >= 1 and table_column[0].valtype == "int") or (
#                     len(map_exp) >= 1 and map_exp[0].val_type in standard):
#                 round_tag = True
#             # analysis sensitivity
#             sens = aggf.sym.sensitivity()
#             if sens is None:
#                 continue
#             aggF_list.append((aggf, sens))
#             # add noise
#             epsilon, _ = privdatas.allocate_cost()
#             noised_expr = laplaceNoiseRewriter(copy.copy(aggf), sens, epsilon, round_tag)
#             privdatas.incrby(epsilon)
#             # replace with noised agg
#             replace_use_of(aggf, noised_expr)
#
#     relations = parsed_sql.source.relations
#     for relation in relations:
#         primary = relation.primary
#         if type(primary) == AliasedSubquery:
#             logging.debug("noise_addition_rewriter subquery: " + str(primary.query))
#             noise_addition_rewriter(primary.query, privdatas)
