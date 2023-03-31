from tests.unit_test.utils import DPSQL_TEST
from differential_privacy.accountant.accountant import PrivDataGroup
import math


def test_add_gaussian_noise():
    dbconfig = {'test': 'tob_apps_all', 'reader': 'clickhouse', 'database': 'default', 'host': 'test'}
    table_list = ['test']
    privdatas = PrivDataGroup()
    privdatas.init(table_list, dbconfig)
    method = 'gauss'
    traceid = 'traceid'
    row_in = (3338436.0, 6639, 3338436.0, 0)
    sensitivities = (1410.0, 1, 1410.0, None)
    epsilons = [0.9, 0.9, 0.9, 0]
    delts = [1e-08, 1e-08, 1e-08, 0]
    min_val = [None, None, None, None]
    agg = ['sum', 'count', 'sum', None]
    out_row = DPSQL_TEST._add_noise(row_in, sensitivities, privdatas, epsilons, delts, traceid, min_val, agg, method)
    out_row_len = len(out_row)
    assert len(row_in) == len(out_row)
    for i in range(out_row_len):
        if sensitivities[i] is None:
            assert out_row[i] == 0
        else:
            assert math.isclose(row_in[i], out_row[i], rel_tol=0.5)
