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

import math
import numpy as np
from differential_privacy.accountant.noise import laplace_utility


def laplace_error(eps, sens):
    if sens is None:
        return None
    beta = 0.1
    alpha = laplace_utility(sens, eps, beta)
    # the utility means: with the probability of at least (1-beta), the error of result is less than alpha
    return {"max_error": round(alpha, 5), "min_prob": 1 - beta}


def get_avg_utility(sum_info, count_info):
    eps_s, sens_s, s_hat = sum_info
    eps_c, sens_c, c_hat = count_info
    beta = 0.1
    ln_2_beta = math.log(2 / beta)
    flag = 2 / eps_c * ln_2_beta
    if c_hat > flag:
        bound = sens_s * ln_2_beta / (eps_s * c_hat) + \
            2 * np.abs(s_hat) * ln_2_beta / (eps_c * c_hat * c_hat) + \
            2 * sens_s * (ln_2_beta * ln_2_beta) / (eps_s * eps_c * c_hat * c_hat)
        return {"max_error": round(bound, 5), "min_prob": 1 - beta}
    else:
        return None


def zip_para(noise_data_list, epsilons, sensitivities, source_col_names):
    para_dict = dict((scn, (eps, sens, noise)) for noise, eps, sens, scn in zip(noise_data_list, epsilons, sensitivities, source_col_names))
    return para_dict


def get_utility_dict(noise_data_list, epsilons, sensitivities, source_col_names, rewritten_sql):
    bindings = zip_para(noise_data_list, epsilons, sensitivities, source_col_names)
    all_utility_dict = {}
    m_symbols = rewritten_sql.select_block.m_symbols
    for sym in m_symbols:
        sym_name = sym[0]
        sym_expression = sym[1]
        sym_utility = None
        if sym_name in bindings:
            sens = bindings[sym_name][1]
            if sens is None:
                sym_utility = None
            else:
                if hasattr(sym_expression, "type"):
                    if sym_expression.type.name == 'Identifier_EXPR':
                        # eps, sens, noise
                        sym_utility = laplace_error(bindings[sym_name][0], bindings[sym_name][1])
        else:
            if hasattr(sym_expression, "type"):
                if sym_expression.type.name == 'NestedExpression_EXPR':
                    nested_expr = sym_expression.expr
                    if nested_expr.type.name == 'DivideExpression_EXPR':
                        sum_info = bindings[nested_expr.left.text]
                        count_info = bindings[nested_expr.right.text]
                        sym_utility = get_avg_utility(sum_info, count_info)
        all_utility_dict[sym_name] = sym_utility
    return all_utility_dict
