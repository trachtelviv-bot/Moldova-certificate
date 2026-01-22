def collect_form_data(vars_dict):
    return {k: v.get() for k, v in vars_dict.items()}

