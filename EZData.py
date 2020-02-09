import re
import random
import math


########################################################################################################################


class SucceededValidation:
    pass


class FailedValidation:
    pass


class Error(Exception):
    pass


class IdentifierDoesntMatchValue(Error):
    pass


def IdentifierDoesntMatchValueRaiser(identifier, value):
    error_end = {
        'null': 'The only allowed value is: null',
        'boolean': 'Allowed values are: true / false',
        'number': 'Allowed values are: any number including floating points and negatives.',
        'string': 'Make sure to have matching quotes at start and end of string',
        'array': 'Make sure to include array elements between [ and ]',
        'map': 'Make sure to include map elements between { and }',
    }

    message = 'Type of %s doesn\'t match %s identifier. %s' % (identifier, value, error_end.get(identifier))
    return IdentifierDoesntMatchValue(message)


class UnknownIdentifier(Error):
    pass


def UnknownIdentifierRaiser(value):
    message = 'Uknown identifier for value %s.' % value
    return IdentifierDoesntMatchValue(message)


class EmptyValue(Error):
    pass


def EmptyValueRaiser(value, identifier):
    def place_of_empty_valu(v):
        i = v.index('')
        if i == 0:
            return 'The first value in the array is empty.'
        elif i == len(v) - 1:
            return 'The last value in the array is empty.'
        else:
            return 'Empty value is between %s and %s at index %s' % (i - 1, i + 1, i)

    errors = {
        'array': 'Can\'t declare an array with an empty value. %s' % place_of_empty_valu(value),
        'map': 'Can\'t declare an map with an empty value. %s' % place_of_empty_valu(value),
        'map-key': 'Can\'t create a key,value pair with empty key',
        'map-value': 'Can\'t create a key,value pair with empty value, '
                     'you can use null as map value if you need an empty map value',
    }

    return EmptyValue(errors.get(identifier))


class InvalidKeyValuePairStructure(Error):
    pass


def InvalidKeyValuePairStructureRaiser(value):
    message = 'Make sure to have one value for every key, got %s values for the same key.' % value.count(':')
    return InvalidKeyValuePairStructure(message)


class UsageOfReservedWord(Error):
    pass


def UsageOfReservedWordRaiser(reserved_word):
    message = 'Can\'t use a reserved word %s as a name or value.' % reserved_word
    return UsageOfReservedWord(message)


class BadVariableName(Error):
    pass


def BadVariableNameRaiser(name):
    message = 'Variable name must start with a letter or underscore, got %s' % name
    return BadVariableName(message)


class VariableNotFound(Error):
    pass


def VariableNotFoundRaiser(value):
    message = 'Can\'t find a variable with the name: %s' % value
    return VariableNotFound(message)


class BadSyntax(Error):
    pass


def BadSyntaxRaiser(command, correct_syntax):
    message = 'Bad syntax provided, %s doesnt match the syntax %s.' % (command, correct_syntax)
    return BadSyntax(message)


class UnknownOperation(Error):
    pass


def UnknownOperationRaiser(op):
    message = 'Unknown operation: %s' % op
    return UnknownOperation(message)


class WrongOperationArgumentType(Error):
    pass


def WrongOperationArgumentTypeRaiser(op, arg, required_type):
    message = 'Operation %s require arguments of type %s, got %s.' % (op, required_type, arg)
    return WrongOperationArgumentType(message)


class WrongOperationArgumentCount(Error):
    pass


def WrongOperationArgumentCountRaiser(op, required_args_count, command):
    message = 'Operation %s requires %s arguments, got %s' % (op, required_args_count, command)
    return WrongOperationArgumentCount(message)


class MissingFor(Error):
    pass


def MissingForRaiser(what, where):
    message = 'Missing %s for %s' % (what, where)
    raise MissingFor(message)


########################################################################################################################


def join_pairs(pairs):
    _res = []
    for i in pairs:
        f = False
        for k in _res:
            if i[0] > k[0] and i[1] < k[1]:
                f = True
                continue
            elif i[0] < k[0] and i[1] > k[1]:
                f = True
                _res[_res.index(k)] = i
        if not f:
            _res.append(i)

    return list(set(_res))


def find_matching_parens(s, open_par, close_par):
    result = []
    parens_stack = []

    for i, c in enumerate(s):
        if c == open_par:
            parens_stack.append(i)
        elif c == close_par:
            if len(parens_stack) == 0:
                raise MissingForRaiser('closing parentheses in %s at %s' % (s, str(i)), ']')
            result.append((parens_stack.pop(), i))
    if len(parens_stack) > 0:
        raise MissingForRaiser('opening parentheses in %s at %s' % (s, str(parens_stack.pop())), ']')
    return result


def variable_exists(var_name):
    return var_name.__hash__ is not None and var_name in VARIABLES


def delete_variable(var_name):
    if variable_exists(var_name):
        del VARIABLES[var_name]

    return VariableNotFoundRaiser(var_name)


def find_type(value):
    if type(value) is not str:
        value = str(value)

    if value == '':
        return [UnknownIdentifierRaiser("''")]

    if variable_exists(value):
        var = VARIABLES.get(value)
        return [var.get('class_name'), var.get('value')]

    for var_type in VARIABLE_TYPES:
        if re.fullmatch(VARIABLE_TYPES[var_type]['structure'], value):
            _ = VARIABLE_TYPES[var_type]['checker'](value)
            if _[0] is SucceededValidation:
                return [var_type, _[1]]

    if value in RESERVED_WORDS:
        return [UsageOfReservedWordRaiser(value)]

    return [UnknownIdentifierRaiser(value)]


def array_checker(value):
    if value == '[]':
        return SucceededValidation, []

    res = []
    value = value[1:-1]
    brackets = sorted(join_pairs(find_matching_parens(value, '[', ']') + find_matching_parens(value, '{', '}')),
                      key=lambda i: i[0])
    value_split = [i.strip().replace(', ', ',').replace(' ,', ',') for i in [value[:brackets[0][0]]] +
                   [value[brackets[i - 1][1] + 1:brackets[i][0]] for i in range(1, len(brackets))] +
                   [value[brackets[-1][1] + 1:]]] if len(brackets) > 0 else [value]

    for i in range(len(value_split)):
        values = value_split[i].split(',')

        if len(brackets) > 0:
            if i == 0:
                if values[-1] != '':
                    return FailedValidation, EmptyValueRaiser(value, 'array')
                values = values[:-1]
            elif i == len(value_split) - 1:
                if values[0] != '':
                    return FailedValidation, EmptyValueRaiser(value, 'array')
                values = values[1:]
            else:
                if '' not in [values[0], values[-1]]:
                    return FailedValidation, EmptyValueRaiser(value, 'array')
                values = values[1:-1]

        if i > 0:
            br = brackets[i - 1]
            if value[br[0]] == '[' and value[br[-1]] == ']':
                _ = array_checker(value[br[0]: br[1] + 1])
                if _[0] is FailedValidation:
                    return _
                res.append(_[1])
            elif value[br[0]] == '{' and value[br[-1]] == '}':
                _ = map_checker(value[br[0]: br[1] + 1])
                if _[0] is FailedValidation:
                    return _
                res.append(_[1])
            else:
                return FailedValidation, BadSyntaxRaiser(value[br[0] + 1: br[1]],
                                                         '[<elements>]' if br[0] is '[' else '{<pairs>}')

        for j in range(len(values)):
            _ = run_command(values[j])
            if _[0] is SucceededValidation:
                res.append(_[1])
            else:
                return FailedValidation, _[1]

    return SucceededValidation, res


def map_checker(value):
    if value == '{}':
        return SucceededValidation, {}

    res = {}
    value = value[1:-1]
    brackets = sorted(join_pairs(find_matching_parens(value, '[', ']') + find_matching_parens(value, '{', '}')),
                      key=lambda i: i[0])
    value_split = [i.strip().replace(', ', ',').replace(' ,', ',') for i in [value[:brackets[0][0]]] +
                   [value[brackets[i - 1][1] + 1:brackets[i][0]] for i in range(1, len(brackets))] +
                   [value[brackets[-1][1] + 1:]]] if len(brackets) > 0 else [value]

    full_pair_regex = r'(?:(?:(?P<quote>[\'\"])([_a-zA-Z]\w*)(?P=quote))|([_a-zA-Z]\w*))\s*:\s*(.+)'
    only_key_regex = r'(?:(?:(?P<quote>[\'\"])([_a-zA-Z]\w*)(?P=quote))|([_a-zA-Z]\w*))\s*:\s*'

    for i in range(len(value_split)):
        values = [i.strip() for i in value_split[i].split(',') if i != '']

        for j in range(len(values)):
            if not re.fullmatch(full_pair_regex, values[j]):
                if j < len(values) - 1 or not re.fullmatch(only_key_regex, values[j]):
                    return FailedValidation, InvalidKeyValuePairStructureRaiser(value)

            if j < len(values) - 1 or \
                    re.fullmatch(full_pair_regex, values[j]):
                _ = re.findall(full_pair_regex, values[j])[0]
                key = _[1] or _[2]
                _ = run_command(_[-1])
                if _[0] is SucceededValidation:
                    _value = _[1]
                    res = {**res, **{key: _value}}
                else:
                    return FailedValidation, _[1]
            elif i > 0:
                br = brackets[i - 1]
                key = re.findall(only_key_regex, values[j])[0]

                if value[br[0]] == '[' and value[br[-1]] == ']':
                    _ = array_checker(value[br[0]: br[1] + 1])
                    if _[0] is FailedValidation:
                        return _
                    res = {**res, **{key: _[1]}}
                elif value[br[0]] == '{' and value[br[-1]] == '}':
                    _ = map_checker(value[br[0]: br[1] + 1])
                    if _[0] is FailedValidation:
                        return _
                    res = {**res, **{key: _[1]}}
                else:
                    return FailedValidation, BadSyntaxRaiser(value[br[0] + 1: br[1]],
                                                             '[<elements>]' if br[0] is '[' else '{<pairs>}')

    return SucceededValidation, res


########################################################################################################################


def find_else_end(lines, key='if'):
    i = 1
    _ = 1
    _else = -1
    _endif = -1
    problem = -1

    while i < len(lines):
        if re.fullmatch(r'\s*' + key + r'.*', lines[i]):
            _ += 1
            problem = i
        elif re.fullmatch(r'\s*end\s+' + key + r'\s*', lines[i]):
            if _ <= 0:
                raise MissingForRaiser('an %s statement' % key, 'end %s statement inside of %s scope' % (key, lines[0]))
            if _ > 1:
                _ -= 1
                problem = -1
            else:
                _endif = i
                break
        elif re.fullmatch(r'\s*else\s*', lines[i]) and _ == 1 and _else < 0:
            _else = i

        i += 1

    if i == len(lines):
        raise MissingForRaiser('<end %s>' % key, lines[problem])

    return _else, _endif


def run_command(command, previous_ops=None):
    if command is None or previous_ops == []:
        return SucceededValidation, command

    command = command.strip()

    command_is_var = find_type(command)
    if len(command_is_var) > 1:
        return SucceededValidation, command_is_var[1]

    _c = re.compile(r'([\'"].*[\'"])').sub(r"", command)

    if '(' in _c:
        start, end = find_matching_parens(command, '(', ')')[-1]
        inner = run_command(command[start + 1: end])

        if inner[0] is FailedValidation:
            raise inner[1]

        return run_command(command[:start] + inner[1] + command[end + 1:])

    ops = sorted(sorted([op for op in OPERATIONS if op in _c], key=lambda op: -OPERATIONS[op]['power']),
                 key=lambda op: -len(re.findall(OPERATIONS[op]['structure'], command)))

    if len(ops) == 0:
        raise UnknownOperationRaiser(command)

    operation = ops[0]

    match = re.search(OPERATIONS[operation]['structure'], command)
    groups = re.findall(OPERATIONS[operation]['structure'], command) if match is not None else None
    _ = groups[0] if type(groups[0]) is tuple else groups

    if groups is None or not OPERATIONS[operation]['args_expected'](len(_)):
        raise BadSyntaxRaiser(command, OPERATIONS[operation]['correct_form'])

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
            raise BadSyntaxRaiser(command, OPERATIONS[operation]['correct_form'])

        _groups = []
        for i in _:
            if i != '':
                _groups.append(i)

    result = OPERATIONS[operation]['function'](_groups)

    updated_command = command.replace(command[match.start(): match.end()], str(result) if result is not None else '')

    return run_command(updated_command, ops[1:])


def run_file(file_name='main.ezdata'):
    with open(file_name + ('.ezdata' if file_name[-7:] != '.ezdata' else ''), 'r') as file:
        lines = ''.join(file.readlines())

    while '//' in lines:
        lines = ''.join(re.split(r'//.*', lines))

    while '/*' in lines:
        lines = ''.join(re.split(r'/\*.*?\*/', lines))

    run_lines([i.strip() for i in lines.split('\n') if i != ''])


def run_lines(lines):
    i = 0

    while i < len(lines):
        if len(lines[i].strip()) == 0:
            pass
        elif re.fullmatch(r'\s*if.*', lines[i]):
            _else, _end = find_else_end(lines[i:])
            _else += (i if _else > -1 else 0)
            _end += i
            condition = run_command(re.findall(r'if\s+(.*)', lines[i])[0])

            if condition[0] is FailedValidation:
                raise condition[1]

            if find_type(condition[1])[1]:
                run_lines(lines[i + 1: (_else if _else > -1 else _end)])
            elif _else > -1:
                run_lines(lines[_else + 1: _end])

            i = _end
        elif re.fullmatch(r'\s*while.*', lines[i]):
            _end = find_else_end(lines[i:], key='while')[1] + i
            condition_text = re.findall(r'while\s+(.*)', lines[i])[0]
            condition = run_command(condition_text)

            if condition[0] is FailedValidation:
                raise condition[1]

            while find_type(condition[1])[1]:
                run_lines(lines[i + 1: _end])
                condition = run_command(condition_text)

                if condition[0] is FailedValidation:
                    raise condition[1]

            i = _end
        elif re.fullmatch(r'\s*for\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)\s*', lines[i]):
            _end_for = find_else_end(lines[i:], key='for')[1] + i
            _ = re.findall(r'\s*for\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)\s*', lines[i])

            if len(_) == 0:
                raise

            counter, start, end = _[0]
            if re.fullmatch(r'(.+?)\s+jump\s+(.+)', end):
                end, jump = re.findall(r'(.+?)\s+jump\s+(.+)', end)[0]
            else:
                jump = 1

            if jump == '':
                jump = 1

            _start, _end, _jump = find_type(start), find_type(end), find_type(jump)

            if _start[0] is not 'number':
                raise WrongOperationArgumentTypeRaiser('for-from-to', start, 'number')

            if _end[0] is not 'number':
                raise WrongOperationArgumentTypeRaiser('for-from-to', end, 'number')

            if _jump[0] is not 'number':
                raise WrongOperationArgumentTypeRaiser('for-from-to', jump, 'number')

            for j in range(_start[1], _end[1], _jump[1]):
                run_set([counter, str(j)])
                run_lines(lines[i + 1: _end_for])

            delete_variable(counter)

            i = _end_for
        elif re.fullmatch(r'\s*for\s+(.+?)\s+in\s+(.+?)\s*', lines[i]):
            _end_for = find_else_end(lines[i:], key='for')[1] + i
            _ = re.findall(r'\s*for\s+(.+?)\s+in\s+(.+?)\s*', lines[i])

            if len(_) == 0:
                raise

            counter, where = _[0]
            _where = find_type(where)

            if _where[0] not in ['array', 'map']:
                raise WrongOperationArgumentTypeRaiser('for-in', where, 'collection (Array / Map)')

            for j in _where[1]:
                run_set([counter, str(j)])
                run_lines(lines[i + 1: _end_for])

            delete_variable(counter)

            i = _end_for

        else:
            run_command(lines[i])

        i += 1


def run_print(groups):
    def __format(txt):
        txt = '"%s"' % txt if type(txt) is str else txt
        if len(find_type(txt)) == 1:
            raise find_type(txt)[0]
        _, _value = find_type(txt)
        if _ == 'null':
            formatted = 'null'
        elif _ == 'boolean':
            formatted = 'true' if re.fullmatch(r'[tT]rue', str(txt)) else 'false'
        elif _ == 'string':
            formatted = txt[1:-1]
            if len(formatted) >= 2:
                if formatted[0] == formatted[-1] and formatted[0] in ['"', "'"]:
                    formatted = formatted[1:-1]
        elif _ == 'array':
            formatted = '[' + ', '.join([str(__format(i)) for i in _value]) + ']'
        elif _ == 'map':
            formatted = '{' + ', '.join(['%s: %s' % (str(__format(i)), str(__format(_value[i]))) for i in _value]) + '}'
        elif _ is SucceededValidation:
            formatted = _value
        else:
            formatted = txt
        return formatted

    output = re.split(r'\s+end\s+with\s+', groups[0])

    text = run_command(output[0])
    end = '\n'

    if text[0] is FailedValidation:
        raise text[1]

    if len(output) == 2:
        end = run_command(output[1])

        if end[0] is FailedValidation:
            raise end[1]

        type_of_end = find_type(end[1])

        if type_of_end[0] is 'string':
            end = type_of_end[1][1:-1]
        else:
            raise WrongOperationArgumentTypeRaiser('print <output> end with <end>', output[1], 'string')

    msg = text[1][1:-1] if type(text[1]) is str else text[1]

    print(__format(msg), end=end)


def run_input(groups):
    _ = ''

    if len(groups) == 1:
        msg = run_command(groups[0])

        if msg[0] is FailedValidation:
            raise msg[1]

        type_of_msg = find_type(msg[1])

        if type_of_msg[0] is 'string':
            _ = type_of_msg[1]
        else:
            raise WrongOperationArgumentTypeRaiser('input message <message>', groups[0], 'string')

    return "'%s'" % input(_[1:-1])


def run_typeof(groups):
    var = run_command(groups[0])

    if var[0] is FailedValidation:
        raise var[1]

    var_type = find_type(var[1])

    if len(var_type) == 1:
        raise var_type[0]

    return "'%s'" % var_type[0]


def run_set(groups):
    if re.fullmatch(r'[a-zA-Z_]\w*', groups[0]):
        var_name = groups[0]
    else:
        raise BadVariableNameRaiser(groups[0])

    var_value = run_command(groups[1])

    if var_name[0] is FailedValidation:
        raise var_name[1]

    if var_value[0] is FailedValidation:
        raise var_value[1]

    var_type = find_type(str(var_value[1]))

    if len(var_type) == 1:
        raise var_type[0]

    VARIABLES[var_name] = {'class_name': var_type[0], 'value': var_value[1]}


def run_shuffle(groups):
    _op = run_command(groups[0])

    if _op[0] is FailedValidation:
        raise _op[1]

    if find_type(_op[1])[0] is not 'array':
        raise WrongOperationArgumentTypeRaiser('shuffle', groups[0], 'array')

    arr = find_type(_op[1])[1]
    random.shuffle(arr)

    if re.fullmatch(r'[_a-zA-Z]\w*', groups[0]):
        run_set((groups[0], str(arr)))

    return arr


def run_n_arg_op(n, groups, op, f, _type=None, _types=None):
    ops = []
    for i in range(n):
        _ = run_command(groups[i])
        if _[0] is FailedValidation:
            raise _[1]
        if _types and all(find_type(_[1])[0] is not i for i in _types):
            raise WrongOperationArgumentTypeRaiser(op, groups[i], ' / '.join(_types))
        elif _type and find_type(_[1])[0] is not _type:
            raise WrongOperationArgumentTypeRaiser(op, groups[i], _type)
        ops.append(_[1])

    return f(*ops)


def run_pick(groups):
    if len(groups) == 3:
        start, end, jump = run_n_arg_op(3, groups, 'pick number', lambda *args: args, _type='number')
    else:
        start, end = run_n_arg_op(2, groups, 'pick number', lambda *args: args, _type='number')
        jump = 1

    return random.randrange(start, stop=end, step=jump)


########################################################################################################################

VARIABLE_TYPES = {
    'null': {
        'structure': r'null|None',
        'checker': lambda value: (SucceededValidation, None)
    },
    'boolean': {
        'structure': r'([tT]rue)|([fF]alse)',
        'checker': lambda value: (SucceededValidation, True if re.fullmatch(r'[tT]rue', value) else False)
    },
    'number': {
        'structure': r'(\-)?(\d+)(\.\d+)?',
        'checker': lambda value: (SucceededValidation, int(value) if re.fullmatch(r'-?\d+', value) else float(value))
    },
    'string': {
        'structure': r'\'\'|\"\"|(?P<quote>[\'\"]).*?[^\\](?P=quote)',
        'checker': lambda value: (SucceededValidation, value)
    },
    'array': {
        'structure': r'\[.*\]',
        'checker': array_checker
    },
    'map': {
        'structure': r'\{((?:(?:(?P<quote>[\'\"])([_a-zA-Z]\w*)(?P=quote))|([_a-zA-Z]\w*))\s*\:\s*(.*?))*\s*\}',
        'checker': map_checker
    }
}
OPERATIONS = {
    'print': {
        'structure': r'print\s+(\([^\)]*\)|.*)',
        'function': run_print,
        'correct_form': 'print <output> (end with <end>)',
        'power': -1,
        'args_expected': lambda i: 2 >= i >= 1
    },
    'input': {
        'structure': r'input\s*?(?: message\s+(\S.*))?',
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
        'structure': r'del\s+([_a-zA-Z]\w*)',
        'function': lambda groups: delete_variable(groups[0]),
        'correct_form': 'del <var_name>',
        'power': 0,
        'args_expected': lambda i: i == 1
    },
    '+': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+[+]\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, '+', lambda a, b: a + b, _type='number'),
        'correct_form': '<operator1> + <operator2>',
        'power': 6,
        'args_expected': lambda i: i == 2
    },
    '- ': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+[-]\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, '-', lambda a, b: a - b, _type='number'),
        'correct_form': '<operator1> - <operator2>',
        'power': 6,
        'args_expected': lambda i: i == 2
    },
    '* ': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+[*]\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, '*', lambda a, b: a * b, _type='number'),
        'correct_form': '<operator1> * <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    '/': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+[/]\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, '/', lambda a, b: a / b, _type='number'),
        'correct_form': '<operator1> / <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    '%': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+[%]\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, '%', lambda a, b: a % b, _type='number'),
        'correct_form': '<operator1> % <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    'raise': {
        'structure':
            r'raise\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))\s+to\s+power\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(2, groups, 'raise to power', lambda a, b: a ** b, _type='number'),
        'correct_form': 'raise <operator> to power <power>',
        'power': 8,
        'args_expected': lambda i: i == 2
    },
    'sqrt': {
        'structure': r'sqrt\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*))',
        'function': lambda groups: run_n_arg_op(1, groups, 'sqrt', lambda x: x ** 0.5, _type='number'),
        'correct_form': 'sqrt of <operator>',
        'power': 8,
        'args_expected': lambda i: i == 1
    },
    'or': {
        'structure': r'(\S+)\s+or\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'or', lambda a, b: a or b, 'number',
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> or <operator2>',
        'power': 1,
        'args_expected': lambda i: i == 2
    },
    'xor': {
        'structure': r'(\S+)\s+xor\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'xor', lambda a, b: a ^ b, 'number',
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> xor <operator2>',
        'power': 1.5,
        'args_expected': lambda i: i == 2
    },
    'and': {
        'structure': r'(\S+)\s+and\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'and', lambda a, b: a and b, _types=['number', 'boolean']),
        'correct_form': '<operator1> and <operator2>',
        'power': 2,
        'args_expected': lambda i: i == 2
    },
    'not': {
        'structure': r'not\s+(\S+)',
        'function': lambda groups: run_n_arg_op(1, groups, 'not', lambda x: not x, _types=['number', 'boolean']),
        'correct_form': 'not <operator>',
        'power': 3,
        'args_expected': lambda i: i == 1
    },
    'shift left': {
        'structure': r'(\S+)\s+shift left\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'shift left', lambda a, b: a << b,
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> shift left <operator2>',
        'power': 5,
        'args_expected': lambda i: i == 2
    },
    'shift right': {
        'structure': r'(\S+)\s+shift right\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'shift right', lambda a, b: a >> b,
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> shift right <operator2>',
        'power': 5,
        'args_expected': lambda i: i == 2
    },
    'equals': {
        'structure': r'(\S+)\s+equals\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'equals', lambda a, b: a == b),
        'correct_form': '<operator1> equals <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'different from': {
        'structure': r'(\S+)\s+different from\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'different from', lambda a, b: a != b),
        'correct_form': '<operator1> different from <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'greater than': {
        'structure': r'(\S+)\s+greater than\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'greater than', lambda a, b: a > b,
                                                _types=['number', 'string', 'boolean', 'array']),
        'correct_form': '<operator1> greater than <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'smaller than': {
        'structure': r'(\S+)\s+smaller than\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'smaller than', lambda a, b: a < b,
                                                _types=['number', 'string', 'boolean', 'array']),
        'correct_form': '<operator1> smaller than <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'greater or equal than': {
        'structure': r'(\S+)\s+greater or equal than\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'greater or equal', lambda a, b: a >= b,
                                                _types=['number', 'string', 'boolean', 'array']),
        'correct_form': '<operator1> greater or equal than <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'smaller or equal than': {
        'structure': r'(\S+)\s+smaller or equal than\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'smaller or equal', lambda a, b: a <= b,
                                                _types=['number', 'string', 'boolean', 'array']),
        'correct_form': '<operator1> smaller or equal than <operator2>',
        'power': 4,
        'args_expected': lambda i: i == 2
    },
    'pick from': {
        'structure': r'pick\s+from\s+(\S.*)',
        'function': lambda groups: run_n_arg_op(1, groups, 'pick from', lambda i: random.choice(i), _type='array'),
        'correct_form': 'pick from <array>',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    'shuffle': {
        'structure': r'shuffle\s+([_a-zA-Z]\w*)',
        'function': run_shuffle,
        'correct_form': 'shuffle <array>',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    'pick number': {
        'structure': r'pick\s+number\s+start\s+(\S+)\s+stop\s+(\S+)\s*?(?: jump\s+(\S.*))?',
        'function': run_pick,
        'correct_form': 'pick number start <start> stop <end> (jump <jump>)',
        'power': 10,
        'args_expected': lambda i: 3 >= i >= 2
    },
}
RESERVED_WORDS = list(VARIABLE_TYPES.keys()) + list(OPERATIONS.keys())
VARIABLES = {}
FUNCTIONS = {}

if __name__ == '__main__':
    run_file()
