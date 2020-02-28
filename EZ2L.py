import math
import os
import random
import re
import time


########################################################################################################################


class Null:
    text = 'null'


class SucceededValidation:
    pass


class FailedValidation:
    pass


class Error(Exception):
    pass


class UnknownIdentifier(Error):
    pass


def UnknownIdentifierRaiser(value):
    message = 'Uknown identifier for value <%s>.' % value
    return UnknownIdentifier(message)


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
    message = 'Can\'t use a reserved word <%s> as a name or value.' % reserved_word
    return UsageOfReservedWord(message)


class BadVariableName(Error):
    pass


def BadVariableNameRaiser(name):
    message = 'Variable name must start with a letter or underscore, got <%s>' % name
    return BadVariableName(message)


class VariableNotFound(Error):
    pass


def VariableNotFoundRaiser(value):
    message = 'Can\'t find a variable with the name <%s>' % value
    return VariableNotFound(message)


class BadSyntax(Error):
    pass


def BadSyntaxRaiser(command, correct_syntax):
    message = 'Bad syntax provided, <%s> doesnt match the syntax <%s>.' % (command, correct_syntax)
    return BadSyntax(message)


class UnknownOperation(Error):
    pass


def UnknownOperationRaiser(op):
    message = 'Unknown operation <%s>' % op
    return UnknownOperation(message)


class WrongOperationArgumentType(Error):
    pass


def WrongOperationArgumentTypeRaiser(op, arg, required_type):
    message = 'Operation <%s> require arguments of type <%s>, got <%s>.' % (op, required_type, arg)
    return WrongOperationArgumentType(message)


class WrongOperationArgumentCount(Error):
    pass


def WrongOperationArgumentCountRaiser(op, required_args_count, got):
    message = 'Operation <%s> requires <%s> arguments, got <%s>' % (op, required_args_count, got)
    return WrongOperationArgumentCount(message)


class MissingFor(Error):
    pass


def MissingForRaiser(what, where):
    message = 'Missing <%s> for <%s>' % (what, where)
    raise MissingFor(message)


class NotIn(Error):
    pass


def NotInRaiser(command, _com, _in):
    message = '<%s> in <%s> must be in <%s> scope' % (_com, command, _in)
    return NotIn(message)


class TooMany(Error):
    pass


def TooManyRaiser(what, _in, required):
    message = 'Too many <%s> in <%s>, only %s required' % (what, _in, required)
    return TooMany(message)


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


def check_usage_of_reserved_word(value):
    if value in VARIABLE_TYPES or value in OPERATIONS or value in CLASSES or value in FUNCTIONS:
        raise UsageOfReservedWordRaiser(value)


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

    check_usage_of_reserved_word(value)

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

    full_pair_regex = r'(?:(?:(?P<quote>[\'\"])(%s)(?P=quote))|(%s))\s*:\s*(.+)' % (var_r, var_r)
    only_key_regex = r'(?:(?:(?P<quote>[\'\"])(%s)(?P=quote))|(%s))\s*:\s*' % (var_r, var_r)

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


def find_else_end(lines, key='if', key2='else'):
    i = 1
    _ = 1
    _else = -1
    _endif = -1

    while i < len(lines):
        if re.fullmatch(r'\s*' + key + r'.*', lines[i]):
            _ += 1
        elif re.fullmatch(r'\s*end\s+' + key + r'\s*', lines[i]):
            if _ <= 0:
                raise MissingForRaiser('an %s statement' % key, 'end %s statement inside of %s scope' % (key, lines[0]))
            if _ > 1:
                _ -= 1
            else:
                _endif = i
                break
        elif re.fullmatch(r'\s*%s\s*' % key2, lines[i]) and _ == 1 and _else < 0:
            _else = i

        i += 1

    if i == len(lines):
        raise MissingForRaiser('<end %s>' % key, lines[0])

    return _else, _endif


def get_function_args(__args):
    _args = []
    temp = ''
    _i = 0
    while _i < len(__args):
        if __args[_i] in '[{':
            _i = find_matching_parens(__args[_i:], __args[_i], {'[': ']', '{': '}'}.get(__args[_i]))[0][0]
        elif __args[_i] == ',':
            _args.append(temp)
            temp = ''
        else:
            temp += __args[_i]
        _i += 1
    _args.append(temp)
    args_without_formatting = __args
    args = []

    for _i in _args:
        if _i.strip() != '':
            if '=' in _i:
                arg_name, default = re.findall(r'(%s)\s*=\s*(.*)' % var_r, _i.strip())[0]
            else:
                arg_name, default = _i.strip(), None
            args.append((arg_name.strip(), default))

    return args, args_without_formatting


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


def run_import(groups):
    filename = groups[0]
    if not re.match(r'(.*)\.ez2l', filename):
        filename += '.ez2l'

    if os.path.isfile(filename):
        run_file(filename)
    else:
        raise FileNotFoundError('File %s not found' % groups[0])


def run_print(groups):
    def _format(txt):
        _type, _value = find_type(txt)
        formatted = {
            'number': lambda i: str(i),
            'boolean': lambda i: 'true' if i else 'false',
            'null': lambda i: Null.text,
            'string': lambda i: i[1:-1].encode('utf-8').decode('unicode_escape'),
            'array': lambda i: '[%s]' % ', '.join([_format(j) for j in i]),
            'map': lambda i: '{%s}' % ', '.join(['%s: %s' % (j, _format(i[j])) for j in i])
        }.get(_type, lambda i: i)(_value)
        return formatted.replace('""', '"', formatted.count('"') // 2).encode('utf-8').decode('unicode_escape')

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

    print(_format(text[1]), end=end)


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

    var = var[0], (var[1] if var[1] is not Null else 'null')
    var_type = find_type(var[1])

    if len(var_type) == 1:
        raise var_type[0]

    return "'%s'" % (var_type[0] if var_type[0] is not Null else 'null')


def run_set(groups, _ret=False):
    if re.fullmatch(r'[a-zA-Z_]\w*', groups[0]) or groups[0] in VARIABLES:
        var_name = groups[0]
    else:
        raise BadVariableNameRaiser(groups[0])

    if type(groups[1]) is not tuple:
        var_value = run_command(groups[1])
        if var_value[1] is Null:
            var_value = var_value[0], 'null'

        if var_value[0] is FailedValidation:
            raise var_value[1]

        var_type = find_type(str(var_value[1]))
        if len(var_type) == 1:
            raise var_type[0]

        var_type = var_type[0]
        var_value = var_value[1]
    else:
        var_type = groups[1][0]
        var_value = groups[1][1]

    var = {
        'class_name': var_type,
        'value': var_value
    }

    if _ret:
        return var_name, var

    VARIABLES[var_name] = var


def run_shuffle(groups):
    _op = run_command(groups[0])

    if _op[0] is FailedValidation:
        raise _op[1]

    if find_type(_op[1])[0] is not 'array':
        raise WrongOperationArgumentTypeRaiser('shuffle', groups[0], 'array')

    arr = find_type(_op[1])[1]
    random.shuffle(arr)

    if re.fullmatch(instance_r, groups[0]):
        run_set((groups[0], str(arr)))

    return arr


def run_add(groups):
    collection = run_command(groups[1])

    if find_type(collection[1])[0] not in ['array', 'string', 'map']:
        raise WrongOperationArgumentTypeRaiser('shuffle', groups[0], 'array/string/map')

    collection = find_type(collection[1])[1]

    element = run_command('{%s}' % groups[0]
                          if re.findall(VARIABLE_TYPES.get('map').get('structure'), '{%s}' % groups[0])
                          else groups[0])[1]

    if type(collection) is str:
        if type(element) is not str:
            raise BadSyntaxRaiser('add to string', 'add \"<STRING> to <string>')
        collection = '"%s"' % (collection[1:-1] + element[1:-1])
    elif type(collection) is list:
        if type(element) is not list:
            raise BadSyntaxRaiser('add to array', 'add [elements] to <array>')
        collection = list(collection) + list(element)
    else:
        if type(element) is not dict:
            raise BadSyntaxRaiser('add to map', 'add <key>:<value> to <map>')
        collection = {**collection, **element}

    if re.fullmatch(instance_r, groups[1]):
        run_set((groups[1], str(collection)))

    return collection


def run_pick(groups):
    if len(groups) == 3:
        start, end, jump = run_n_arg_op(3, groups, 'pick number', lambda *args: args, _type='number')
    else:
        start, end = run_n_arg_op(2, groups, 'pick number', lambda *args: args, _type='number')
        jump = 1

    return random.randrange(start, stop=end, step=jump)


def run_dir(groups):
    path = run_command(groups[0])[1][1:-1]
    ret = []

    for (dirpath, dirnames, filenames) in os.walk(path):
        if len(groups) == 1:
            ret.extend(filenames + dirnames)
        elif groups[1] == 'files':
            ret.extend(filenames)
        else:
            ret.extend(dirnames)
        break

    return ret


def run_function(name, normal=None):
    def inner(groups):
        func = normal if normal else FUNCTIONS.get(name)
        optional = [i.strip() for i in func.get('args') if func.get('args').get(i) is not None]
        required = [i.strip() for i in func.get('args') if func.get('args').get(i) is None]
        final_args = {}
        previous = {}
        _args = []
        temp = ''
        if len(groups) > 0:
            i = 0
            while i < len(groups[0]):
                if groups[0][i] in '[{':
                    i = find_matching_parens(groups[0][i:], groups[0][i], {'[': ']', '{': '}'}.get(groups[0][i]))[0][0]
                elif groups[0][i] == ',':
                    _args.append(temp)
                    temp = ''
                else:
                    temp += groups[0][i]
                i += 1
            _args.append(temp)

        args = [run_command(i) for i in _args]
        for _ in range(len(args)):
            if args[_][0] is FailedValidation:
                raise args[_][1]
            args[_] = args[_][1]

        if len(args) < len(required) or len(args) > len(func.get('args')):
            raise WrongOperationArgumentCountRaiser(name, 'between %s and %s' %
                                                    (len(required), len(func.get('args'))), len(args))

        for i in range(len(required)):
            final_args[required[i]] = args[i]

        for i in range(len(optional)):
            if i + len(required) < len(args):
                final_args[optional[i]] = args[i + len(required)]
            else:
                final_args[optional[i]] = func.get('args').get(optional[i])

        for i in final_args:
            if i in VARIABLES:
                previous[i] = VARIABLES.get(i).get('value')
            run_set((i, str(final_args[i])))

        result = run_lines(func.get('code'), _in='function')

        for i in final_args:
            if i in previous:
                run_set((i, str(previous.get(i))))
            else:
                del VARIABLES[i]

        return result

    return lambda groups: inner(groups)


def run_create(groups):
    instance = groups[0]
    check_usage_of_reserved_word(instance)

    class_name = groups[1]
    if class_name not in CLASSES:
        raise VariableNotFoundRaiser(class_name)
    cls = CLASSES[class_name]

    for i in cls.get('variables'):
        VARIABLES['%s.%s' % (instance, i)] = {
            'class_name': 'null',
            'value': 'null'
        }

    for f in cls.get('functions'):
        f_name = re.findall(r'function\s+(%s)\(.+' % var_r, f)[0]
        f_body = [i % (('%s' % instance,) * i.count('%s')) if '%s' in i else i for i in cls.get('functions')[f]]
        run_lines_function([f.replace(f_name, '%s.%s' % (instance, f_name))] + f_body + ['end function'], 0, False)

    run_function('%s constructor' % class_name, {
        'args': cls.get('constructor').get('args'),
        'code': [i % (('%s' % instance,) * i.count('%s')) if '%s' in i else i for i in cls.get('constructor')['code']]
    })([groups[2]])

    VARIABLES[instance] = {
        'class_name': class_name,
        'value': {i: VARIABLES.get('%s.%s' % (instance, i)) for i in cls.get('variables')}
    }

    return instance


def run_command(command, previous_ops=None):
    if command is None or previous_ops == [] or command == '':
        return SucceededValidation, command

    command = command.strip()
    command_is_var = find_type(command)
    if len(command_is_var) > 1:
        return SucceededValidation, command_is_var[1]

    _c = re.compile(r'([\'"].*[\'"])').sub(r"", command)

    if '(' in _c:
        f = re.findall(r'.*?\s*(%s)\s*\(.*?\)' % instance_r, command)
        if len(f) == 0 or (f[0] not in FUNCTIONS and f[0] not in CLASSES):
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
    _ = groups[0] if groups is not None and type(groups[0]) is tuple else groups
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
    updated_command = command.replace(command[match.start(): match.end()],
                                      str(result) if result is not None else 'null')

    return run_command(updated_command, ops[1:])


def run_lines_if(lines, i, _in):
    _else, _end = find_else_end(lines[i:])
    _else += (i if _else > -1 else 0)
    _end += i
    condition = run_command(re.findall(r'if\s+(.*)', lines[i])[0])

    if condition[0] is FailedValidation:
        raise condition[1]

    if find_type(condition[1])[1]:
        result = run_lines(lines[i + 1: (_else if _else > -1 else _end)], _in=_in)
    elif _else > -1:
        result = run_lines(lines[_else + 1: _end], _in=_in)
    else:
        result = None
    return _end, result


def run_lines_try(lines, i, _in):
    _catch, _end = find_else_end(lines[i:], key='try', key2='catch')
    _catch += (i if _catch > -1 else 0)
    _end += i

    try:
        result = run_lines(lines[i + 1: (_catch if _catch > -1 else _end)], _in=_in)
    except:
        if _catch > -1:
            result = run_lines(lines[_catch + 1: _end], _in=_in)
        else:
            result = None

    return _end, result


def run_lines_while(lines, i, _in):
    _end = find_else_end(lines[i:], key='while')[1] + i
    condition_text = re.findall(r'while\s+(.*)', lines[i])[0]
    condition = run_command(condition_text)

    if condition[0] is FailedValidation:
        raise condition[1]

    while find_type(condition[1])[1]:
        result = run_lines(lines[i + 1: _end], _in=_in)
        condition = run_command(condition_text)

        if condition[0] is FailedValidation:
            raise condition[1]

        if result is not None:
            return _end, result

    return _end, None


def run_lines_for_from_to(lines, i, _in):
    _end_for = find_else_end(lines[i:], key='for')[1] + i
    _ = re.findall(r'\s*for\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)\s*', lines[i])

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

    previous = None if counter not in VARIABLES else VARIABLES.get(counter).get('value')
    for j in range(_start[1], _end[1], _jump[1]):
        run_set([counter, str(j)])
        result = run_lines(lines[i + 1: _end_for], _in=_in)
        if result is not None:
            return _end_for, result

    delete_variable(counter)

    if previous:
        run_set((counter, str(previous)))

    return _end_for, None


def run_lines_for_in(lines, i, _in):
    _end_for = find_else_end(lines[i:], key='for')[1] + i
    _ = re.findall(r'\s*for\s+(.+?)\s+in\s+(.+?)\s*', lines[i])

    counter, where = _[0]
    _where = find_type(where)

    if _where[0] not in ['array', 'map']:
        raise WrongOperationArgumentTypeRaiser('for-in', where, 'collection (Array / Map)')

    previous = None if counter not in VARIABLES else VARIABLES.get(counter).get('value')
    for j in _where[1]:
        run_set([counter, str(j)])
        result = run_lines(lines[i + 1: _end_for], _in=_in)
        if result is not None:
            return _end_for, result

    delete_variable(counter)
    if previous:
        run_set((counter, str(previous)))

    return _end_for, None


def run_lines_function(lines, i, normal=True):
    _end_function = find_else_end(lines[i:], key='function')[1] + i
    code = lines[i + 1: _end_function]
    if normal:
        regex = r'\s*function\s+(%s)\s*\((.*?)\)\s*' % var_r
    else:
        regex = r'\s*function\s+(.+?)\s*\((.*?)\)\s*'
    _ = re.findall(regex, lines[i])[0]

    name, args = _

    check_usage_of_reserved_word(name)

    args, args_without_formatting = get_function_args(args)

    FUNCTIONS[name] = {
        'args': dict(args),
        'code': code
    }
    OPERATIONS[name] = {
        'structure': r'%s\s*\((.*?)\)' % name,
        'function': run_function(name),
        'correct_form': '%s(%s)' % (name, args_without_formatting),
        'power': 10,
        'args_expected': lambda _i: _i == 1
    }

    del name
    return _end_function, None


def run_lines_return(lines, i, _in):
    if _in != 'function':
        raise NotInRaiser(lines[i], 'return', 'function')
    result = run_command(re.findall(r'\s*return\s+(.*)\s*', lines[i])[0].strip())[1]
    return result if result is not Null else 'null'


def get_class_variables(_class_name, _class_body):
    variables = re.findall(r'variables\s*(.*?)\s*end\s+variables', ''.join(_class_body), flags=re.DOTALL)
    class_variables = {}
    if len(variables) > 1:
        raise TooManyRaiser('values scope', _class_name, 1)
    if len(variables) > 0:
        variables_scope_start = _class_body.index('variables')
        variables_scope_end = find_else_end(_class_body[variables_scope_start:], key='variables')[1]
        for variable in _class_body[variables_scope_start + 1: variables_scope_end + variables_scope_start]:
            _ = run_set(('%s' % variable, 'null'), _ret=True)
            class_variables[_[0]] = _[1]

    return class_variables


def get_class_constructor(_class_name, _class_body, missing_for_where):
    constructor_start = [i for i in range(len(_class_body))
                         if re.fullmatch(r'\s*constructor\s*\((.*?)\)\s*', _class_body[i])]
    if len(constructor_start) == 0:
        raise MissingForRaiser('constructor', missing_for_where)
    if len(constructor_start) > 1:
        raise TooManyRaiser('constructor', _class_name, 1)
    constructor_start = constructor_start[0]
    constructor_end = find_else_end(_class_body[constructor_start:], key='constructor')[1] + constructor_start
    constructor_body = _class_body[constructor_start + 1: constructor_end]

    return get_function_args(
        re.findall(r'constructor\s*\((.*?)\)', _class_body[constructor_start])[0]
    ), constructor_body


def run_lines_class(lines, _i):
    _class_name = re.findall(r'\s*class\s+(%s)\s*' % var_r, lines[_i])[0]
    _end_class = find_else_end(lines[_i:], key='class')[1] + _i
    _class_body = lines[_i + 1: _end_class]

    class_variables = get_class_variables(_class_name, _class_body)
    constructor_head, constructor_body = get_class_constructor(_class_name, _class_body, lines[_i])
    functions = {_class_body[i]: _class_body[i + 1:find_else_end(_class_body[i:], key='function')[1] + i]
                 for i in range(len(_class_body))
                 if re.fullmatch(r'\s*function\s+(%s)\s*\((.*?)\)\s*' % var_r, _class_body[i])}
    functions_items = list(functions.items())

    for _f in range(len(functions) + 1):
        if _f == 0:
            _code_ = constructor_body
        else:
            _code_ = functions_items[_f - 1][1]
        for i in range(len(_code_)):
            j = 0
            while j < len(_code_[i]) - len(_class_name):
                if _code_[i][j] in '\'"':
                    j = find_matching_parens(_code_[i][j:], _code_[i][j], _code_[i][j])[0][1]
                elif _code_[i][j:j + len(_class_name)] == _class_name:
                    _ = [k for k in _code_[i]]
                    _[j:j + len(_class_name)] = '%s'
                    _code_[i] = ''.join(_)
                    j = j + 2
                j += 1

        if _f > 0:
            functions[functions_items[_f - 1][0]] = _code_

    CLASSES[_class_name] = {
        'variables': class_variables,
        'constructor': {
            'args_without_formatting': constructor_head[1],
            'args': dict(constructor_head[0]),
            'code': constructor_body
        },
        'functions': functions
    }

    return _end_class, None


def run_lines(lines, _in=None):
    i = 0

    while i < len(lines):
        if len(lines[i].strip()) == 0:
            pass
        elif re.fullmatch(r'\s*try\s*', lines[i]):
            i = run_lines_try(lines, i, _in)
        elif re.fullmatch(r'\s*if.*', lines[i]):
            i = run_lines_if(lines, i, _in)
        elif re.fullmatch(r'\s*while.*', lines[i]):
            i = run_lines_while(lines, i, _in)
        elif re.fullmatch(r'\s*for\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)\s*', lines[i]):
            i = run_lines_for_from_to(lines, i, _in)
        elif re.fullmatch(r'\s*for\s+(.+?)\s+in\s+(.+?)\s*', lines[i]):
            i = run_lines_for_in(lines, i, _in)
        elif re.fullmatch(r'\s*function\s+(%s)\s*\((.*?)\)\s*' % var_r, lines[i]):
            i = run_lines_function(lines, i)
        elif re.fullmatch(r'\s*return\s+(.*)\s*', lines[i]):
            return run_lines_return(lines, i, _in)
        elif re.fullmatch(r'\s*class\s+(%s)\s*' % var_r, lines[i]):
            i = run_lines_class(lines, i)
        else:
            run_command(lines[i])
        if type(i) is tuple:
            if i[1] is not None:
                return i[1]
            i = i[0]
        i += 1

    return None


def run_file(file_name='main.ez2l'):
    with open(file_name + ('' if re.fullmatch(r'(.*?)\.ez2l', file_name) else '.ez2l'), 'r') as file:
        lines = ''.join(file.readlines())

    while '//' in lines:
        lines = ''.join(re.split(r'//.*', lines))

    while '/*' in lines:
        lines = ''.join(re.split(r'/\*.*?\*/', lines, flags=re.DOTALL))

    run_lines([i.strip() for i in lines.split('\n') if i != ''])


########################################################################################################################

var_r = r'[_a-zA-Z]\w*'
instance_r = r'[_a-zA-Z]\w*(?:\.[_a-zA-Z]\w*)*'
instance_number_r = r'(?:\-?\d+(?:\.\d+)?)+|(?:%s)' % instance_r
str_arr_map_r = r'(?:\'\'|\"\"|(?P<squote>[\'\"]).*?[^\\](?P=squote))|(?:\[.*\])|' \
                r'(?:\{(?:(?:(?:(?P<quote>[\'\"])[_a-zA-Z]\w*(?P=quote))|[_a-zA-Z]\w*)\s*\:\s*(?:.*?))*\s*\})'
d_instance_r = (instance_r, instance_r)
VARIABLE_TYPES = {
    'null': {
        'structure': r'null|None',
        'checker': lambda value: (SucceededValidation, Null)
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
        'structure': r'(?P<squote>[\'\"]).*(?P=squote)',
        'checker': lambda value: (SucceededValidation, '"%s"' % value[1:-1])
    },
    'array': {
        'structure': r'\[.*\]',
        'checker': array_checker
    },
    'map': {
        'structure': r'\{((?:(?:(?P<quote>[\'\"])(%s)(?P=quote))|(%s))\s*\:\s*(.*?))*\s*\}' % (var_r, instance_r),
        'checker': map_checker
    }
}
OPERATIONS = {
    'import': {
        'structure': r'import\s+(.*)',
        'function': run_import,
        'correct_form': 'import <file_name>',
        'power': -1,
        'args_expected': lambda i: i == 1
    },
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
    'create': {
        'structure': r'create\s+(%s)\s+from\s+(%s)\s+initialize\s+with\s*(.*)' % (var_r, var_r),
        'function': run_create,
        'correct_form': 'create <instance_name> from <class_name> initialize with <args>',
        'power': 20,
        'args_expected': lambda i: i == 3
    },
    'set': {
        'structure': r'set\s+(%s)\s+to\s+(\S.*)' % instance_r,
        'function': run_set,
        'correct_form': 'set <var_name> to <value>',
        'power': 0,
        'args_expected': lambda i: i == 2
    },
    'del': {
        'structure': r'del\s+(%s)' % var_r,
        'function': lambda groups: delete_variable(groups[0]),
        'correct_form': 'del <var_name>',
        'power': 0,
        'args_expected': lambda i: i == 1
    },
    'typeof': {
        'structure': r'typeof\s+(\S.*)',
        'function': run_typeof,
        'correct_form': 'typeof <var>',
        'power': 0,
        'args_expected': lambda i: i == 1
    },

    # Collection Operations
    'get': {
        'structure': r'get\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))\s+from\s+(%s|%s)' % (instance_r, instance_r, str_arr_map_r),
        'function': lambda groups: run_n_arg_op(2, groups, 'get', lambda i, j: (j[1:-1] if type(j) is str else j)[i]),
        'correct_form': 'get <index> from <operator>',
        'power': 5,
        'args_expected': lambda i: i == 4
    },
    'in': {
        'structure': r'(.+?)\s+in\s+(%s|%s)' % (str_arr_map_r, instance_r),
        'function': lambda groups: run_n_arg_op(2, groups, 'in', lambda i, j: i in j),
        'correct_form': '<element> in <operator>',
        'power': 5,
        'args_expected': lambda i: i == 4
    },
    'add': {
        'structure': r'add\s+(.+?)\s+to\s+(%s|%s)' % (str_arr_map_r, instance_r),
        'function': run_add,
        'correct_form': 'add <element> to <operator>',
        'power': 5,
        'args_expected': lambda i: i == 4
    },
    'slice': {
        'structure': r'slice\s+(%s|%s)\s+from\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))\s+to\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' %
                     (str_arr_map_r, instance_r, instance_r, instance_r),
        'function': lambda groups: run_n_arg_op(3, [groups[0]] + groups[2:4] if groups[1] in ['"', "'"] else groups,
                                                'slice',
                                                lambda i, j, k: ('"%s"' % i[j:k] if type(i) is str else i[j:k])),
        'correct_form': 'slice <operator> from <start> to <end>',
        'power': 5,
        'args_expected': lambda i: i == 5
    },

    # Logical Operations
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
    'bitand': {
        'structure': r'(%s)\s+bitand\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, 'bitand', lambda a, b: a & b, 'number',
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> bitand <operator2>',
        'power': 5,
        'args_expected': lambda i: i == 2
    },
    'bitor': {
        'structure': r'(%s)\s+bitor\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, 'bitor', lambda a, b: a | b, 'number',
                                                _types=['number', 'boolean']),
        'correct_form': '<operator1> bitor <operator2>',
        'power': 5,
        'args_expected': lambda i: i == 2
    },
    'bitnot': {
        'structure': r'bitnot\s+(%s)' % instance_number_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'bitnot', lambda a: ~ a, 'number',
                                                _types=['number', 'boolean']),
        'correct_form': 'bitnot <operator2>',
        'power': 5,
        'args_expected': lambda i: i == i
    },

    # Comparison Operations
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

    # Random Operations
    'pick from': {
        'structure': r'pick\s+from\s+(\S.*)',
        'function': lambda groups: run_n_arg_op(1, groups, 'pick from', lambda i: random.choice(i), _type='array'),
        'correct_form': 'pick from <array>',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    'shuffle': {
        'structure': r'shuffle\s+(%s)' % instance_r,
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

    # Numeric Operations
    '+': {
        'structure': r'(%s)\s+[+]\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, '+', lambda a, b: a + b, _type='number'),
        'correct_form': '<operator1> + <operator2>',
        'power': 6,
        'args_expected': lambda i: i == 2
    },
    '- ': {
        'structure': r'(%s)\s+[-]\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, '-', lambda a, b: a - b, _type='number'),
        'correct_form': '<operator1> - <operator2>',
        'power': 6,
        'args_expected': lambda i: i == 2
    },
    '* ': {
        'structure': r'(%s)\s+[*]\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, '*', lambda a, b: a * b, _type='number'),
        'correct_form': '<operator1> * <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    '/': {
        'structure': r'(%s)\s+[/]\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, '/', lambda a, b: a / b, _type='number'),
        'correct_form': '<operator1> / <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    '%': {
        'structure': r'((?:\-?\d+(?:\.\d+)?)+|(?:[_a-zA-Z]\w*(?:\.[_a-zA-Z]\w*)*))\s+[\%]\s+((?:\-?\d+(?:\.\d+)?)+|'
                     r'(?:[_a-zA-Z]\w*(?:\.[_a-zA-Z]\w*)*))',
        'function': lambda groups: run_n_arg_op(2, groups, '%', lambda a, b: a % b, _type='number'),
        'correct_form': '<operator1> % <operator2>',
        'power': 7,
        'args_expected': lambda i: i == 2
    },
    'raise': {
        'structure': r'raise\s+(%s)\s+to\s+power\s+(%s)' % (instance_number_r, instance_number_r),
        'function': lambda groups: run_n_arg_op(2, groups, 'raise to power', lambda a, b: a ** b, _type='number'),
        'correct_form': 'raise <operator> to power <power>',
        'power': 8,
        'args_expected': lambda i: i == 2
    },
    'sqrt': {
        'structure': r'sqrt\s+of\s+(%s)' % instance_number_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'sqrt', lambda x: x ** 0.5, _type='number'),
        'correct_form': 'sqrt of <operator>',
        'power': 8,
        'args_expected': lambda i: i == 1
    },
    'abs': {
        'structure': r'abs\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'abs', lambda i: abs(i), _type='number'),
        'correct_form': 'abs <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'floor': {
        'structure': r'floor\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'floor', lambda i: math.floor(i), _type='number'),
        'correct_form': 'floor of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'ceil': {
        'structure': r'ceil\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'ceil', lambda i: math.ceil(i), _type='number'),
        'correct_form': 'ceil of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'ln': {
        'structure': r'ln\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'ln', lambda i: math.log(i, math.e), _type='number'),
        'correct_form': 'ln <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'log': {
        'structure':
            r'log\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))\s+base\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % d_instance_r,
        'function': lambda groups: run_n_arg_op(2, groups, 'floor', lambda i, j: math.log(i, j), _type='number'),
        'correct_form': 'log <operator> base <base>',
        'power': 5,
        'args_expected': lambda i: i == 2
    },
    'sin': {
        'structure': r'sin\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'sin', lambda i: math.sin(i), _type='number'),
        'correct_form': 'sin <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'cos': {
        'structure': r'cos\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'cos', lambda i: math.cos(i), _type='number'),
        'correct_form': 'cos <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'tan': {
        'structure': r'tan\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'tan', lambda i: math.tan(i), _type='number'),
        'correct_form': 'tan <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'asin': {
        'structure': r'asin\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'asin', lambda i: math.asin(i), _type='number'),
        'correct_form': 'asin <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'acos': {
        'structure': r'acos\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'acos', lambda i: math.acos(i), _type='number'),
        'correct_form': 'acos <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'atan': {
        'structure': r'atan\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'atan', lambda i: math.atan(i), _type='number'),
        'correct_form': 'atan <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'sinh': {
        'structure': r'sinh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'sinh', lambda i: math.sinh(i), _type='number'),
        'correct_form': 'sinh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'cosh': {
        'structure': r'cosh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'cosh', lambda i: math.cosh(i), _type='number'),
        'correct_form': 'cosh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'tanh': {
        'structure': r'tanh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'tanh', lambda i: math.tanh(i), _type='number'),
        'correct_form': 'tanh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'asinh': {
        'structure': r'asinh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'asinh', lambda i: math.asinh(i), _type='number'),
        'correct_form': 'asinh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'acosh': {
        'structure': r'acosh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'acosh', lambda i: math.acosh(i), _type='number'),
        'correct_form': 'acosh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'atanh': {
        'structure': r'atanh\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'atanh', lambda i: math.atanh(i), _type='number'),
        'correct_form': 'atanh <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'factorial': {
        'structure': r'factorial\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'factorial', lambda i: math.factorial(i), _type='number'),
        'correct_form': 'factorial of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'degrees': {
        'structure': r'degrees\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'degrees', lambda i: math.degrees(i), _type='number'),
        'correct_form': 'degrees of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'radians': {
        'structure': r'radians\s+of\s+((?:\-?\d+(?:\.\d+)?)+|(?:%s))' % instance_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'radians', lambda i: math.radians(i), _type='number'),
        'correct_form': 'radians of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 1
    },
    'length': {
        'structure': r'length\s+of\s+(%s|%s)' % (str_arr_map_r, instance_r),
        'function': lambda groups: run_n_arg_op(1, groups, 'length', lambda i: len(i) - (2 if type(i) is str else 0),
                                                _types=['array', 'string', 'map']),
        'correct_form': 'length of <operator>',
        'power': 5,
        'args_expected': lambda i: i == 3
    },

    # Time Operations
    'time': {
        'structure': r'(time)',
        'function': lambda groups: time.time(),
        'correct_form': 'time',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    'ctime': {
        'structure': r'ctime\s+(%s)' % instance_number_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'ctime', lambda i: time.ctime(i), _type='number'),
        'correct_form': 'ctime <seconds>',
        'power': 10,
        'args_expected': lambda i: i == 1
    },
    'sleep': {
        'structure': r'sleep\s+(%s)' % instance_number_r,
        'function': lambda groups: run_n_arg_op(1, groups, 'sleep', lambda i: time.sleep(i), _type='number'),
        'correct_form': 'sleep <seconds>',
        'power': 20,
        'args_expected': lambda i: i == 1
    },

    # Files Operations
    'dir': {
        'structure': r'dir\s+(\S+)(?:\s+only\s+(files|dirs))?',
        'function': run_dir,
        'correct_form': 'dir <path> (only files|dirs)',
        'power': 20,
        'args_expected': lambda i: 2 >= i >= 1
    },
    'create file': {
        'structure': r'create\s+file\s+(\S.*)\s+at\s+(\S.*)',
        'function': lambda groups: run_n_arg_op(2, groups, 'create file',
                                                lambda i, j: open(os.path.join(j[1:-1], i[1:-1]), 'w+')
                                                , _type='string'),
        'correct_form': 'create file <filename> at <path>',
        'power': 20,
        'args_expected': lambda i: i == 2
    },
    'delete file': {
        'structure': r'delete\s+file\s+(\S.*)',
        'function': lambda groups: run_n_arg_op(1, groups, 'delete file', lambda i: os.remove(i[1:-1]), _type='string'),
        'correct_form': 'delete file <filepath>',
        'power': 20,
        'args_expected': lambda i: i == 1
    },
    'read': {
        'structure': r'read\s+from\s+(\S.*)',
        'function': lambda groups: run_n_arg_op(1, groups, 'read',
                                                lambda i: [j.strip() for j in open(i[1:-1], 'r').readlines()]
                                                , _type='string'),

        'correct_form': 'read from <filepath>',
        'power': 20,
        'args_expected': lambda i: i == 1
    },
    'write': {
        'structure': r'write\s+(\S.*)\s+to\s+(\S+)',
        'function': lambda groups: run_n_arg_op(2, groups, 'write',
                                                lambda i, j: open(i[1:-1], 'a').write('\n%s' % j[1:-1]),
                                                _type='string'),
        'correct_form': 'write <line> to <filepath>',
        'power': 20,
        'args_expected': lambda i: i == 2
    },
}
VARIABLES = {
    'MATH.E': {
        'class_name': 'number',
        'value': math.e
    },
    'MATH.PI': {
        'class_name': 'number',
        'value': math.pi
    }
}
FUNCTIONS = {}
CLASSES = {}
OBJECTS = {}

if __name__ == '__main__':
    run_file()
