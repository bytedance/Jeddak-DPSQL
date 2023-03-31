from differential_privacy.accountant.budget import BudgetManager
from datetime import datetime


def budget_recover():
    try:
        budget_manager = BudgetManager()
        sql_dict = {
            "budget_table_name": budget_manager.budget_table_name,
        }
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_dict["current_time"] = current_time
        sql_dict["last_update_time"] = current_time
        sql_dict["last_recover_time"] = current_time
        sql_dict["num_dpcall"] = 0
        sql_dict["sum_eps"] = 0
        sql_dict["sum_del"] = 0
        sql_dict["sum_sq_eps"] = 0
        sql_dict["sum_exp_eps"] = 0
        sql_dict["prod_del"] = 1.0
        recover_sql = '''
        UPDATE {budget_table_name} SET
        consumed_budget = 0,
        last_update_time = '{last_update_time}',
        last_recover_time = '{last_recover_time}',
        num_dpcall = {num_dpcall},
        sum_eps = {sum_eps},
        sum_del = {sum_del},
        sum_sq_eps = {sum_sq_eps},
        sum_exp_eps = {sum_exp_eps},
        prod_del = {prod_del}
        WHERE TIMESTAMPDIFF(DAY, last_recover_time, '{current_time}') >= recover_cycle
        '''.format(**sql_dict)
        budget_manager.execute_sql(recover_sql)
        print("budget recover task done.")
    except Exception as err:
        raise ValueError("budget recover task error:" + str(err))
