import json
from http_service.api.v1.query.http_query import dpsql_http_interface_query
from tests.unit_test.utils import DBCONFIG_FOR_CK
from parser.utils import ast_utils
from parser.ast.type.node_type import NodeType


class Request:
    def __init__(self, json):
        self.json = json


def test_clipping_gauss():
    sql = "select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20"
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "Gauss",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_clipping_laplace():
    # sql = '''
    # select sum(case
    #         when page_number >= 10 Then
    #         10
    #         when page_number < 10 Then
    #         10
    #         ELSE
    #         page_number
    #         END) as clipped_sum_A,
    #         count(menu_id)
    #         from menu_page
    #         group by menu_id limit 20
    #     '''

    # sql = '''
    # select sum(page_number), count(menu_id) from menu_page group by menu_id limit 20
    # '''

    sql = '''
        select avg(menu_id) from menu_page group by menu_id limit 20
        '''

    # sql = '''
    #     select sum(menu_id) from menu_page group by menu_id limit 20
    #     '''

    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "LAPLACE",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_clipping_laplace_2():
    sql = '''
    select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20
    '''
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "LAPLACE",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_clipping_laplace_3():
    sql = '''
        select varPop(page_number) from menu_page group by menu_id limit 20
    '''
    # sql = '''
    #         select stddevPop(page_number) from menu_page group by menu_id limit 20
    #     '''
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "LAPLACE",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


def test_create_case_when_node():
    sql_expr1 = "CASE WHEN page_number >= 10 THEN 10 WHEN page_number < 10 THEN 10 ELSE page_number END"
    expr1_ast = ast_utils.createExprNode(sql_expr1)
    nodes1 = ast_utils.findNodes(expr1_ast, NodeType.WhenExpression_EXPR)
    nodes2 = ast_utils.findNodes(expr1_ast, NodeType.CaseExpression_EXPR)
    nodes3 = ast_utils.findNodes(expr1_ast, NodeType.CondExpression_EXPR)
    assert len(nodes1) == 2
    assert len(nodes2) == 1
    assert len(nodes3) == 3


def test_debug():
    sql_list = [
        "SELECT sum (c1) FROM (select count(page_number) as c1 from menu_page group by page_number)",  # correct, done
        # "select count(menu_page.menu_id) from menu_page inner join (select id from menu) as v2 on v2.id=menu_page.menu_id",  # TODO[ningning]: test failed
        # "SELECT sum (c1) FROM (select count(menu_id) as c1 from menu_page group by menu_id)",  # correct, done
        # "select sum(c) from (select sum(menu.id) as c from menu join menu_page ON menu_page.menu_id=menu.id join menu_item ON menu_item.menu_page_id=menu_page.id limit 10)", # correct, done
    ]
    sql = sql_list[0]
    key = {
        "sql": sql,
        "dbconfig": DBCONFIG_FOR_CK,
        "queryconfig": {
            "traceid": "traceid",
        },
        "dpconfig": {
            "dp_method": "LAPLACE",
        },
        "extra": {
            "debug": True,
        }
    }
    request = Request(key)
    res = dpsql_http_interface_query(request)
    json_str = json.loads(res)
    code = json_str['status']['code']
    assert code == 0


if __name__ == '__main__':
    # test_clipping_gauss()
    test_clipping_laplace()
    # test_clipping_laplace_2()
    # test_clipping_laplace_3()
    # test_create_case_when_node()
    # test_debug()
