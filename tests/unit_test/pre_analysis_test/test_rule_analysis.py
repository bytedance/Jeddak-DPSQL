import logging

from analysis.analysis_center import RuleAnalysisCenter
from parser.ast.builder.hive_query_ast_builder import HiveAstBuilder


def _test_security_rule_analysis():
    rac = RuleAnalysisCenter()
    rac.load_rules()


def test_security_rule():
    sql = "select myname from table1 where avg(age) > 10"
    builder = HiveAstBuilder()
    ast = builder.get_query_ast(sql)
    rule_analysis_center = RuleAnalysisCenter()
    rule_engines = rule_analysis_center.load_rules()
    errno = 0
    try:
        for rule_engine in rule_engines:
            rule_engine.excute(ast)
    except Exception as err:
        errno = errno + 1
        logging.warning("err: " + str(err))

    assert errno == 1
