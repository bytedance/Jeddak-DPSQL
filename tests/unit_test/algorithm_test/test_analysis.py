from analysis.pre_analysis_center import PreAnalysisCenter
from differential_privacy.noise.elasticsensitivity import ElasticSensitivity
from metadata.matcher.matcher_factory import get_metamatcher
from parser.ast.builder.clickhouse_query_ast_builder import ClickHouseAstBuilder
from parser.symbol.ast_symbols_loader import load_ast_symbols
from tests.unit_test.utils import DBCONFIG_FOR_CK


# Test whether the multi-table join sensitivity calculation algorithm meets expectations
def test_multy_join_sensitivity():
    sql = 'select count(*) as num from menu inner join menu_page on menu.id = menu_page.menu_id join menu_item on menu_item.menu_page_id = menu_page.id'
    builder = ClickHouseAstBuilder()
    ast = builder.get_query_ast(sql)
    pac = PreAnalysisCenter()
    struct_info = pac.getStructInfo(ast)
    meta_matcher = get_metamatcher(sql, DBCONFIG_FOR_CK, "")
    load_ast_symbols(ast, meta_matcher)
    elastic_sensitivity = ElasticSensitivity()
    ji_list = struct_info.struct_join_info.join_infos
    eps = 0.9
    delt = 1e-8
    smooth_sensitivity = elastic_sensitivity.smooth_elastic_sensitivity(ji_list, eps, delt)
    standard = 31450
    assert int(smooth_sensitivity) == standard
