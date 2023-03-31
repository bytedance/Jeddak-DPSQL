

def init_dpconfig(dpconfig: dict = None):
    if dpconfig is None or dpconfig == "":
        dp_method = "Laplace"
        budget_setting = {
            "epsilon": 0.9,
            "delt": 0,
        }
    else:
        dp_method = dpconfig.get("dp_method")
        if dp_method is None or dp_method == "":
            dp_method = "Laplace"
        budget_setting = dpconfig.get("budget_setting")
        if budget_setting is None or budget_setting == "":
            budget_setting = {
                "epsilon": 0.9,
                "delt": 0,
            }
            if dp_method.lower() in ["gauss"]:
                budget_setting["delt"] = 1e-8
        else:
            epsilon = budget_setting.get("epsilon")
            if epsilon is None or epsilon == "":
                budget_setting["epsilon"] = 0.9
            delt = budget_setting.get("delt")
            if delt is None or delt == "":
                budget_setting["delt"] = 1e-8
    new_dpconfig = {
        "dp_method": dp_method,
        "budget_setting": budget_setting,
    }
    return new_dpconfig
