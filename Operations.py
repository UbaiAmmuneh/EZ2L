from Error import SucceededValidation, FailedValidation
from Variables import *


def convert_to_string(_):
    return str(_) if type_of_variable(_)[0] is not String else "'%s'" % _


def run_command(command, previous_ops=None):
    if command is None or previous_ops == []:
        return SucceededValidation, command

    command_is_var = type_of_variable(command)

    if len(command_is_var) > 1:
        return SucceededValidation, command_is_var[1]

    if '(' in command:
        start, end = Variable.find_parens(command, '(', ')')[-1]
        inner = run_command(command[start + 1: end])

        if inner[0] is FailedValidation:
            raise inner[1]

        return run_command(command[:start] + convert_to_string(inner[1]) + command[end + 1:])

    ops = sorted(sorted([op for op in OPERATIONS if op in command], key=lambda op: -OPERATIONS[op]['power']),
                 key=lambda op: -len(re.findall(OPERATIONS[op]['structure'], command)))

    if len(ops) == 0:
        raise Error.UnknownOperationRaiser(command)

    operation = ops[0]

    match = re.search(OPERATIONS[operation]['structure'], command)
    groups = re.findall(OPERATIONS[operation]['structure'], command) if match is not None else None
    _ = groups[0] if type(groups[0]) is tuple else groups

    if groups is None or not OPERATIONS[operation]['args_expected'](len(_)):
        raise Error.BadSyntaxRaiser(command, OPERATIONS[operation]['correct_form'])

    _groups = []
    for i in _:
        if i != '':
            _groups.append(i)

    if operation == 'or' and _groups[1] == 'equal':
        operation = '%s or equal than' % _groups[0]
        match = re.search(OPERATIONS[operation]['structure'], command)
        groups = re.findall(OPERATIONS[operation]['structure'], command) if match is not None else None
        _ = groups[0] if type(groups[0]) is tuple else groups

        if groups is None or not OPERATIONS[operation]['args_expected'](len(_)):
            raise Error.BadSyntaxRaiser(command, OPERATIONS[operation]['correct_form'])

        _groups = []
        for i in _:
            if i != '':
                _groups.append(i)

    result = OPERATIONS[operation]['function'](_groups)

    updated_command = command.replace(command[match.start(): match.end()],
                                      convert_to_string(result) if result is not None else '')

    return run_command(updated_command, ops[1:])


def run_print(groups):
    output = run_command(groups[0])

    if output[0] is FailedValidation:
        raise output[1]

    if output[1] is not None:
        _ = '\n'
        if len(groups) == 2:
            end = run_command(groups[1])

            if end[0] is FailedValidation:
                raise end[1]

            type_of_end = type_of_variable(end[1])

            if type_of_end[0] is String:
                _ = type_of_end[1]

            else:
                raise Error.WrongOperationArgumentTypeRaiser('print <output> end with <end>', groups[1], 'string')

        print(output[1], end=_)


def run_input(groups):
    _ = ''

    if len(groups) == 1:
        msg = run_command(groups[0])

        if msg[0] is FailedValidation:
            raise msg[1]

        type_of_msg = type_of_variable("'%s'" % msg[1])

        if type_of_msg[0] is String:
            _ = type_of_msg[1]
        else:
            raise Error.WrongOperationArgumentTypeRaiser('input message <message>', groups[0], 'string')

    return "'%s'" % input(_)


def run_typeof(groups):
    var = run_command(groups[0])

    if var[0] is FailedValidation:
        raise var[1]

    var_type = type_of_variable(convert_to_string(var[1]))

    if len(var_type) == 1:
        raise var_type[0]

    return "'%s'" % var_type[0].keyword


def run_set(groups):
    var_name = Variable.check_name(groups[0])
    var_value = run_command(groups[1])

    if var_name[0] is FailedValidation:
        raise var_name[1]

    if var_value[0] is FailedValidation:
        raise var_value[1]

    var_type = type_of_variable(var_name[1])

    if len(var_type) == 1:
        raise var_type[0]

    add_variable(var_name[1], var_type, var_value[1])


def run_del(groups):
    delete_variable(groups[0])


def run_dual_arg_op(groups, op, f, _type, _type_in_words=None, check_for_type=True, _types=None):
    op1 = run_command(groups[0])
    op2 = run_command(groups[1])

    if op1[0] is FailedValidation:
        raise op1[1]

    if op2[0] is FailedValidation:
        raise op2[1]

    if _types:
        if not any(type_of_variable(op1[1])[0] is i for i in _types):
            raise Error.WrongOperationArgumentTypeRaiser(op, groups[0], _type_in_words)

        if not any(type_of_variable(op2[1])[0] is i for i in _types):
            raise Error.WrongOperationArgumentTypeRaiser(op, groups[0], _type_in_words)
    else:
        if check_for_type and type_of_variable(op1[1])[0] is not _type:
            raise Error.WrongOperationArgumentTypeRaiser(op, groups[0], _type_in_words or _type.keyword)

        if check_for_type and type_of_variable(op2[1])[0] is not _type:
            raise Error.WrongOperationArgumentTypeRaiser(op, groups[1], _type_in_words or _type.keyword)

    return f(op1[1], op2[1])


def run_add(groups):
    return run_dual_arg_op(groups, '+', lambda a, b: a + b, Number)


def run_subtract(groups):
    return run_dual_arg_op(groups, '-', lambda a, b: a - b, Number)


def run_multiply(groups):
    return run_dual_arg_op(groups, '*', lambda a, b: a * b, Number)


def run_divide(groups):
    return run_dual_arg_op(groups, '/', lambda a, b: a / b, Number)


def run_modulo(groups):
    return run_dual_arg_op(groups, '%', lambda a, b: a % b, Number)


def run_power(groups):
    return run_dual_arg_op(groups, 'raise to power', lambda a, b: a ** b, Number)


def run_or(groups):
    return run_dual_arg_op(groups, 'or', lambda a, b: a or b, Number, 'number / boolean')


def run_xor(groups):
    return run_dual_arg_op(groups, 'xor', lambda a, b: a ^ b, Number, 'number / boolean')


def run_and(groups):
    return run_dual_arg_op(groups, 'and', lambda a, b: a and b, Number, 'number / boolean')


def run_not(groups):
    op = run_command(groups[0])

    if op[0] is FailedValidation:
        raise op[1]

    if type_of_variable(op[1])[0] is not Number:
        raise Error.WrongOperationArgumentTypeRaiser('not', groups[0], 'boolean')

    return not op[1]


def run_shift_left(groups):
    return run_dual_arg_op(groups, 'shift left', lambda a, b: a << b, Number, 'number / boolean')


def run_shift_right(groups):
    return run_dual_arg_op(groups, 'shift right', lambda a, b: a >> b, Number, 'number / boolean')


def run_equals(groups):
    return run_dual_arg_op(groups, 'equals', lambda a, b: a == b, Boolean, check_for_type=False)


def run_different(groups):
    return run_dual_arg_op(groups, 'different from', lambda a, b: a != b, Boolean, check_for_type=False)


def run_greater(groups):
    return run_dual_arg_op(groups, 'greater than', lambda a, b: a > b, Boolean,
                           _types=[Number, String, Boolean, Array], _type_in_words='Number / Boolean / String / Array')


def run_smaller(groups):
    return run_dual_arg_op(groups, 'smaller than', lambda a, b: a < b, Boolean,
                           _types=[Number, String, Boolean, Array], _type_in_words='Number / Boolean / String / Array')


def run_greater_equal(groups):
    return run_dual_arg_op(groups, 'greater or equal', lambda a, b: a >= b, Boolean,
                           _types=[Number, String, Boolean, Array], _type_in_words='Number / Boolean / String / Array')


def run_smaller_equal(groups):
    return run_dual_arg_op(groups, 'smaller or equal', lambda a, b: a <= b, Boolean,
                           _types=[Number, String, Boolean, Array], _type_in_words='Number / Boolean / String / Array')


OPERATIONS = {
    'print': {
        'structure': r'print\s+(\([^\)]*\)|\S*)(?:\s+end with\s+(\S.*))?',
        'function': run_print,
        'correct_form': 'print <output> (end with <end>)',
        'power': -1,
        'args_expected': lambda i: 2 >= i >= 1
    },
    'input': {
        'structure': r'input\s*(?:message\s+(\S.*))?',
        'function': run_input,
        'correct_form': 'input (message <message>)',
        'power': 10,
        'args_expected': lambda i: 1 >= i >= 0
    },
    'typeof': {
        'structure': r'typeof\s+(\S.*)',
        'function': run_typeof,
        'correct_form': 'typeof <var>',
        'power': 0,
        'args_expected': lambda i: i == 1
    },
    'set': {
        'structure': r'set\s+(\S.*)\s+to\s+(\S.*)',
        'function': run_set,
        'correct_form': 'set <var_name> to <value>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'del': {
        'structure': r'del\s+(\S.*)',
        'function': run_del,
        'correct_form': 'del <var_name>',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    '+': {
        'structure': r'(\S+)\s+[+]\s+([^\s+]+)',
        'function': run_add,
        'correct_form': '<operator1> + <operator2>',
        'power': 1,
        'args_expected': lambda i: i == 2
    },
    '- ': {
        'structure': r'(\S+)\s+[-]\s+([^\s-]+)',
        'function': run_subtract,
        'correct_form': '<operator1> - <operator2>',
        'power': 1,
        'args_expected': lambda i: i == 2
    },
    '* ': {
        'structure': r'(\S+)\s+[*]\s+([^\s*]+)',
        'function': run_multiply,
        'correct_form': '<operator1> * <operator2>',
        'power': 2,
        'args_expected': lambda i: i == 2
    },
    '/': {
        'structure': r'(\S+)\s+[/]\s+([^\s/]+)',
        'function': run_divide,
        'correct_form': '<operator1> / <operator2>',
        'power': 2,
        'args_expected': lambda i: i == 2
    },
    '%': {
        'structure': r'(\S+)\s+[%]\s+([^\s%]+)',
        'function': run_modulo,
        'correct_form': '<operator1> % <operator2>',
        'power': 2,
        'args_expected': lambda i: i == 2
    },
    'raise': {
        'structure': r'raise\s+(\S+)\s+to\s+power\s+(\S+)',
        'function': run_power,
        'correct_form': 'raise <operator> to power <power>',
        'power': 3,
        'args_expected': lambda i: i == 2
    },
    'or': {
        'structure': r'(\S+)\s+or\s+(\S+)',
        'function': run_or,
        'correct_form': '<operator1> or <operator2>',
        'power': 1,
        'args_expected': lambda i: i == 2
    },
    'xor': {
        'structure': r'(\S+)\s+xor\s+(\S+)',
        'function': run_xor,
        'correct_form': '<operator1> xor <operator2>',
        'power': 2,
        'args_expected': lambda i: i == 2
    },
    'and': {
        'structure': r'(\S+)\s+and\s+(\S+)',
        'function': run_and,
        'correct_form': '<operator1> and <operator2>',
        'power': 3,
        'args_expected': lambda i: i == 2
    },
    'not': {
        'structure': r'not\s+(\S+)',
        'function': run_not,
        'correct_form': 'not <operator>',
        'power': 4,
        'args_expected': lambda i: i == 1
    },
    'shift left': {
        'structure': r'(\S+)\s+shift left\s+(\S+)',
        'function': run_shift_left,
        'correct_form': '<operator1> shift left <operator2>',
        'power': 3.5,
        'args_expected': lambda i: i == 2
    },
    'shift right': {
        'structure': r'(\S+)\s+shift right\s+(\S+)',
        'function': run_shift_right,
        'correct_form': '<operator1> shift right <operator2>',
        'power': 3.5,
        'args_expected': lambda i: i == 2
    },
    'equals': {
        'structure': r'(\S+)\s+equals\s+(\S+)',
        'function': run_equals,
        'correct_form': '<operator1> equals <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'different from': {
        'structure': r'(\S+)\s+different from\s+(\S+)',
        'function': run_different,
        'correct_form': '<operator1> different from <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'greater than': {
        'structure': r'(\S+)\s+greater than\s+(\S+)',
        'function': run_greater,
        'correct_form': '<operator1> greater than <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'smaller than': {
        'structure': r'(\S+)\s+smaller than\s+(\S+)',
        'function': run_smaller,
        'correct_form': '<operator1> smaller than <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'greater or equal than': {
        'structure': r'(\S+)\s+greater or equal than\s+(\S+)',
        'function': run_greater_equal,
        'correct_form': '<operator1> greater or equal than <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'smaller or equal than': {
        'structure': r'(\S+)\s+smaller or equal than\s+(\S+)',
        'function': run_smaller_equal,
        'correct_form': '<operator1> smaller or equal than <operator2>',
        'power': 0,
        'args_expected': lambda i: i == 2
    }
}
