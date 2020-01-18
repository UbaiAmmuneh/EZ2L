from Variables import Number

VARIABLES = {'x': {'class_name': Number, 'value': 1}}


def variable_exists(var_name):
    return var_name.__hash__ is not None and var_name in VARIABLES


def get_variable(var_name):
    if variable_exists(var_name):
        return VARIABLES[var_name]
