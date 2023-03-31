from datetime import datetime, date
from utils.config.load_config import load_config
from utils.mysql_client import MysqlClient
import logging


def init_budget_info(prefix: str = None, db_name: str = None, table_name: str = None):
    ''' init budget info table by inserting a new record with prefix, db_name and table_name to it.
    Especially, the total_budget, recover_cycle and exhausted_strategy columns will be set as 1000.0, 30, "reject" by default.

    Args:
        prefix: A str indicating the host of the database
        db_name: A str indicating the database name
        table_name: A str indicating the table name
    '''

    budget_manager = BudgetManager()
    budget_manager.set_budget_info(prefix, db_name, table_name, total_budget=1000.0, recover_cycle=30, exhausted_strategy="reject")
    logging.info("dpaccess-internal init_budget, prefix={}, db_name={}, table_name={}".format(prefix, db_name, table_name))


class BudgetManager:

    def __init__(self, budget_table_name="budget_info"):
        self.budget_table_name = budget_table_name
        self.mysql_client = self._create_mysql_client()

    def _create_mysql_client(self):
        mysql_config = load_config("function_test.ini", "mysql_budget")
        username = mysql_config.get("username")
        password = mysql_config.get("password")
        host = mysql_config.get("host")
        port = mysql_config.get("port")
        db_name = mysql_config.get("database")
        mysql_client = MysqlClient(host=host, user=username, password=password, port=port, db_name=db_name)
        return mysql_client

    def _get_column_name_list(self, description=None):
        column_name_list = []
        for d in description:
            column_name_list.append(d[0])
        return column_name_list

    def execute_sql(self, sql=None):
        conn = self.mysql_client.get_connection()
        cur = conn.cursor()
        res = {
            "data": None,
        }
        try:
            cur.execute(sql)
            if 'select' in sql.lower() or 'show' in sql.lower():
                column_name_list = self._get_column_name_list(cur.description)
                res['data'] = [column_name_list]
                outcome = cur.fetchall()
                res['data'].extend(list(outcome))
            if 'insert' in sql.lower() or 'update' in sql.lower() or 'delete' in sql.lower():
                conn.commit()
            return res
        except Exception as err:
            conn.rollback()
            raise ValueError("execute sql error:" + str(err))
        finally:
            cur.close()
            conn.close()

    def create_budget_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS {table_name} (
            prefix VARCHAR(100) NOT NULL,
            db_name VARCHAR(100) NOT NULL,
            table_name VARCHAR(100) NOT NULL,
            total_budget DOUBLE NOT NULL,
            consumed_budget DOUBLE NOT NULL,
            recover_cycle INT NOT NULL DEFAULT 30,
            exhausted_strategy VARCHAR(100) NOT NULL DEFAULT 'reject',
            create_time DATETIME NOT NULL,
            last_update_time DATETIME NOT NULL,
            last_recover_time DATETIME NOT NULL,
            slack DOUBLE NOT NULL DEFAULT 1e-18,
            num_dpcall INT NOT NULL DEFAULT 0,
            sum_eps DOUBLE NOT NULL DEFAULT 0.0,
            sum_del DOUBLE NOT NULL DEFAULT 0.0,
            sum_sq_eps DOUBLE NOT NULL DEFAULT 0.0,
            sum_exp_eps DOUBLE NOT NULL DEFAULT 0.0,
            prod_del DOUBLE NOT NULL DEFAULT 1.0,
            PRIMARY KEY (prefix, db_name, table_name)
            );
            '''.format(**{"table_name": self.budget_table_name})
        self.execute_sql(sql)

    def set_budget_info(self, prefix: str = None, db_name: str = None, table_name: str = None,
                        total_budget: float = None, recover_cycle: int = None, exhausted_strategy: str = None):
        sql_dict = {
            "budget_table_name": self.budget_table_name,
            "prefix": prefix,
            "db_name": db_name,
            "table_name": table_name,
            "total_budget": total_budget,
            "recover_cycle": recover_cycle,
            "exhausted_strategy": exhausted_strategy
        }
        check_if_record_exist_sql = '''
        select * from {budget_table_name} where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}' limit 1
        '''.format(**sql_dict)
        res = self.execute_sql(check_if_record_exist_sql)
        if len(res["data"]) <= 1:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_dict["consumed_budget"] = 0
            sql_dict["create_time"] = current_time
            sql_dict["last_update_time"] = current_time
            sql_dict["last_recover_time"] = current_time
            insert_sql = '''
            insert into {budget_table_name} (prefix, db_name, table_name, total_budget, recover_cycle, exhausted_strategy,
            consumed_budget, create_time, last_update_time, last_recover_time)
            values ('{prefix}', '{db_name}', '{table_name}', {total_budget}, {recover_cycle},
            '{exhausted_strategy}', {consumed_budget}, '{create_time}', '{last_update_time}', '{last_recover_time}')'''.format(**sql_dict)
            res = self.execute_sql(insert_sql)
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_dict["last_update_time"] = current_time
            basic_sql = '''
            update {budget_table_name}
            set total_budget = {total_budget}, recover_cycle = {recover_cycle}, exhausted_strategy = '{exhausted_strategy}'
            where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}'
            '''.format(**sql_dict)
            res = self.execute_sql(basic_sql)
        return res

    def get_budget_info(self, prefix: str = None, db_name: str = None, table_name: str = None):
        sql_dict = {
            "budget_table_name": self.budget_table_name,
            "prefix": prefix,
            "db_name": db_name,
            "table_name": table_name,
        }
        sql = '''
        select * from {budget_table_name} where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}' limit 1
        '''.format(**sql_dict)
        res = self.execute_sql(sql)
        if len(res['data']) <= 1:
            raise ValueError("budget info does not exist")
        else:
            res['data'] = self.transform_datetime_to_string(res['data'])
        return res

    @staticmethod
    def transform_datetime_to_string(data: list = None):
        for r_id, record in enumerate(data):
            new_record = list(record)
            for id, val in enumerate(new_record):
                if isinstance(val, datetime):
                    new_record[id] = val.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(val, date):
                    new_record[id] = val.strftime("%Y-%m-%d")
            data[r_id] = new_record
        return data
