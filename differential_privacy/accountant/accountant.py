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

import numpy as np
import logging
from exception.enum.privacyaccountant_errors_enum import PrivacyAccountantErrors
from exception.errors import PrivacyAccountantError
from differential_privacy.accountant.budget import BudgetManager
from datetime import datetime


BASIC = 0,
ADVANCED_DRV = 1,
ADVANCED_KOV = 2,
AUTO = 3


class PrivacyData:
    """
        PrivacyData contains the data associated to privacy.
        Basic operations on this data, such as accumulating, uploading and downloading data, are supported.
    """

    def __init__(self):
        self.data = dict()
        self.init()

    def init(self):
        self.budget = {"slack": 1e-18}
        self.account = {
            "num_dpcall": 0, "sum_eps": 0, "sum_del": 0,
            "sum_sq_eps": 0, "sum_exp_eps": 0, "prod_del": 1
        }
        self.data.update(self.budget)
        self.data.update(self.account)

    def __getitem__(self, name):
        """
            overload [] to get self.data: PrivacyData[epsilon/delta/...]
        """
        return self.data[name]

    def __setitem__(self, name, value):
        """
            overload [] to set self.data: PrivacyData[epsilon/delta/...]=value
        """
        self.data[name] = value

    def __str__(self):
        """
            return data as string like "epsilon, delta, ..."
        """
        data_str = ""
        for v in self.data.values():
            data_str += str(v) + ', '
        return data_str[:-2]

    def incrby(self, eps, delt):
        """
            add a single consumption of privacy budget
        """
        if eps <= 0:  # check epsilon>0
            raise PrivacyAccountantError(PrivacyAccountantErrors.EPSILON_NEGATIVE_ERROR.value,
                                         "Epsilon must be positive.")
        self.data["num_dpcall"] += 1
        self.data["sum_eps"] += eps
        self.data["sum_del"] += delt
        self.data["sum_sq_eps"] += eps ** 2
        self.data["sum_exp_eps"] += eps * (np.exp(eps) - 1) / (np.exp(eps) + 1)
        self.data["prod_del"] *= (1 - delt)


class PrivDataGroup:
    """
        PrivDataGroup contains a group of privacy data as a dict
        provide the ability to allocate and accumulate privacy consumption
    """

    def __init__(self):
        self.datas = dict()

    def get_id(self, table_list, dbconfig: dict):  # TODO: need to change for adjusting budget_info
        id = ""
        if "host" in dbconfig:
            id = dbconfig["host"]
        else:
            raise PrivacyAccountantError(PrivacyAccountantErrors.PSM_OR_HOST_NULL.value, "No psm and host in dbconfig")
        id += '*' + dbconfig["database"] + '*'
        id_list = []
        for tb in table_list:
            # in case of specifying database in sql, such as tb.name:rangers.tob_apps_all
            if tb.split(".")[0] == dbconfig["database"]:
                id_list.append(id + tb.split(".")[1])
            else:
                id_list.append(id + tb)
        return id_list

    def init(self, table_list, dbconfig: dict):
        """
            get table's name from the parsed sql,
            and initialize the table name list as key of self.datas
        """
        id_list = self.get_id(table_list, dbconfig)
        self.init_id_list(id_list)

    def init_id_list(self, id_list):
        for id in id_list:
            self.datas[id] = PrivacyData()

    def __getitem__(self, id):
        """
            overload [] to get self.data[id]: PrivacyData()
        """
        return self.datas[id]

    def __setitem__(self, id, value):
        """
            overload [] to set self.data[id]=PrivacyData()
        """
        self.datas[id] = value

    def add_new(self, id):
        self.datas[id] = PrivacyData()

    def incrby(self, eps, delt=0):
        """
            increse accountant data by (epsilon ,delta) for every self.datas[id]
        """
        for id in self.datas.keys():
            self.datas[id].incrby(eps, delt)
            logging.info("dpaccess-internal-dp-new-cost-of-table {}:({},{})".format(
                id, eps, delt))

    def allocate_cost(self, set_epsilon: float = None):
        """
            allocate privacy cost when calling dp mechanism
        """
        if set_epsilon is not None:
            eps = set_epsilon
        else:
            eps = 0.9
        delt = 0
        return eps, delt

    def allocate_cost_gauss(self, set_epsilon: float = None, set_delt: float = None):
        """
            allocate privacy cost when calling dp mechanism
        """
        if set_epsilon is not None:
            eps = set_epsilon
        else:
            eps = 0.9
        if set_delt is not None:
            delt = set_delt
        else:
            delt = 1e-8
        return eps, delt

    def allocate_cost_for_join(self, set_epsilon: float = None, set_delt: float = None):
        if set_epsilon is not None:
            eps = set_epsilon
        else:
            eps = 0.9
        if set_delt is not None:
            delt = set_delt
        else:
            delt = 1e-8
        return eps, delt


class PrivacyAccountant:
    """
    PrivacyAccountant tracks privacy cost accross queries, records every privacy cost
    and update the total privacy accountant.

    DRV10: http://people.seas.harvard.edu/~salil/research/PrivateBoosting-focs.pdf
    KOV15: https://arxiv.org/pdf/1311.0776.pdf

    """

    def __init__(self):
        self.budget_manager = BudgetManager()

    def add_cost(self, privdatas: PrivDataGroup):
        for id in privdatas.datas:
            prefix, db_name, table_name = id.split("*")

            id_account = privdatas.datas[id].account
            local_budget_info = privdatas.datas[id].data

            conn = self.budget_manager.mysql_client.get_connection()
            cur = conn.cursor()

            try:
                res = {
                    "data": None,
                }
                sql_dict = {
                    "budget_table_name": self.budget_manager.budget_table_name,
                    "prefix": prefix,
                    "db_name": db_name,
                    "table_name": table_name,
                }
                sql = '''
                        select * from {budget_table_name} where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}' limit 1
                '''.format(**sql_dict)
                cur.execute(sql)
                column_name_list = self.budget_manager._get_column_name_list(cur.description)
                res['data'] = [column_name_list]
                outcome = cur.fetchall()
                res['data'].extend(list(outcome))
                remote_budget_info = res
                remote_budget_info_dict = dict(zip(remote_budget_info["data"][0], remote_budget_info["data"][1]))
                for key in id_account.keys():
                    if key == "prod_del":
                        remote_budget_info_dict[key] *= local_budget_info[key]
                    else:
                        remote_budget_info_dict[key] += local_budget_info[key]

                sum_eps = remote_budget_info_dict["sum_eps"]
                sum_exp_eps = remote_budget_info_dict["sum_exp_eps"]
                sum_sq_eps = remote_budget_info_dict["sum_sq_eps"]
                slack = remote_budget_info_dict["slack"]
                prod_del = remote_budget_info_dict["prod_del"]

                basic_eps = sum_eps
                adv_drv_eps, adv_del = self.drv_compute(sum_exp_eps, sum_sq_eps, slack, prod_del)
                adv_kov_eps, _ = self.kov_compute(sum_exp_eps, sum_sq_eps, slack, prod_del)

                remote_budget_info_dict["consumed_budget"] = min(basic_eps, adv_drv_eps, adv_kov_eps)

                sql_dict = {
                    "budget_table_name": self.budget_manager.budget_table_name,
                }
                sql_dict.update(remote_budget_info_dict)

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql_dict["last_update_time"] = current_time
                sql = '''
                            update {budget_table_name}
                            set consumed_budget = {consumed_budget},
                            last_update_time = '{last_update_time}',
                            num_dpcall = {num_dpcall},
                            sum_eps = {sum_eps},
                            sum_del = {sum_del},
                            sum_sq_eps = {sum_sq_eps},
                            sum_exp_eps = {sum_exp_eps},
                            prod_del = {prod_del}
                            where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}'
                            '''.format(**sql_dict)
                cur.execute(sql)
                conn.commit()
            except Exception as err:
                conn.rollback()
                raise ValueError("add privacy budget cost to MySQL error:" + str(err))
            finally:
                cur.close()
                conn.close()

    def drv_compute(self, sum_exp_eps, sum_sq_eps, slack, prod_del):
        adv_drv_eps = sum_exp_eps + np.sqrt(2 * sum_sq_eps * np.log(1 / slack))
        adv_del = 1 - (1 - slack) * prod_del
        return (adv_drv_eps, adv_del)

    def kov_compute(self, sum_exp_eps, sum_sq_eps, slack, prod_del):
        adv_kov_eps = sum_exp_eps + np.sqrt(2 * sum_sq_eps * np.log(np.exp(1) + np.sqrt(
            sum_sq_eps) / slack))
        adv_del = 1 - (1 - slack) * prod_del
        return (adv_kov_eps, adv_del)


def record_budget_info(privdatas: PrivDataGroup):
    PrivacyAccountant().add_cost(privdatas)
    print("add cost to mysql done.")


def is_budget_depleted(privdatas: PrivDataGroup):
    budget_manager = BudgetManager()
    for id in privdatas.datas:
        prefix, db_name, table_name = id.split("*")
        sql_dict = {
            "budget_table_name": budget_manager.budget_table_name,
            "prefix": prefix,
            "db_name": db_name,
            "table_name": table_name,
        }
        sql = '''
            select * from {budget_table_name} where prefix = '{prefix}' and db_name = '{db_name}' and table_name = '{table_name}' limit 1
        '''.format(**sql_dict)
        budget_info = budget_manager.execute_sql(sql)
        if len(budget_info["data"]) <= 1:
            raise ValueError("Cannot find the budget info about the queried table: " + prefix + "." + db_name + "." + table_name + ".")
        budget_info_dict = dict(zip(budget_info["data"][0], budget_info["data"][1]))
        if budget_info_dict["total_budget"] <= budget_info_dict["consumed_budget"]:
            if budget_info_dict["exhausted_strategy"] == "reject":
                return True
    return False
