from Variables import Number


RESERVED_WORDS = [
    'boolean', 'number', 'string', 'array', 'map', 'node', 'stack', 'queue', 'tree', 'bstree', 'graph', 'delete_var',
    'typeof', 'print', 'input', 'if', 'else', 'while', 'for', 'from', 'to', 'skip', 'in', 'function', 'return', 'takes',
    'as',
]

VARIABLES = {'x': {'class_name': Number, 'value': 1}}


def variable_exists(var_name):
    return var_name.__hash__ is not None and var_name in VARIABLES


def get_variable(var_name):
    if variable_exists(var_name):
        return VARIABLES[var_name]
