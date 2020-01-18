"""
    Variables
"""

import Error
import Interpreter


class SucceededValidation:
    pass


class FailedValidation:
    pass


def type_of_variable(var, check_variables=True):
    import Storage

    if var in RESERVED_WORDS:
        return [Error.UsageOfReservedWordRaiser(var)]
    temp = None
    for variable_type in VARIABLE_TYPES.values():
        temp = variable_type.validate(var)
        if temp[0] is SucceededValidation:
            return [variable_type, temp[1]]
    if check_variables:
        if Storage.variable_exists(var):
            variable = Storage.get_variable(var)
            return [variable.get('class_name'), variable.get('value')]
    return [temp[1]]


class Variable:
    def __init__(self, var_type, value):
        self.var_type = var_type
        self.value = VARIABLE_TYPES.get(self.var_type)(value)

    @staticmethod
    def check_name(name):
        if name[0].isalpha() or name[0] == '_':
            for i in name[1:]:
                if not i.isalpha() and i != '_' and Number.validate(i)[0] is FailedValidation:
                    return FailedValidation, Error.BadVariableNameRaiser(name, name.index(i))
            return SucceededValidation, name
        else:
            return FailedValidation, Error.BadVariableNameRaiser(name, 0)

    @staticmethod
    def find_parens(s, open_par, close_par):
        toret = []
        pstack = []

        for i, c in enumerate(s):
            if c == open_par:
                pstack.append(i)
            elif c == close_par:
                if len(pstack) == 0:
                    raise IndexError("No matching closing parens at: " + str(i))
                toret.append([pstack.pop(), i])

        if len(pstack) > 0:
            raise IndexError("No matching opening parens at: " + str(pstack.pop()))

        return toret


class Null(Variable):
    def __init__(self, value):
        super().__init__('null', value)

    @staticmethod
    def validate(value):
        if value == 'null':
            return SucceededValidation, None
        return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('null', value)


class Boolean(Variable):
    def __int__(self, value):
        super().__init__('boolean', value)

    @staticmethod
    def validate(value):
        values = {'true': True, 'false': False}
        if value.__hash__ is not None and value in values:
            return SucceededValidation, values.get(value)
        return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('boolean', value)


class Number(Variable):
    def __int__(self, value):
        super().__init__('number', value)

    @staticmethod
    def validate(value):
        try:
            temp = float(value)
            ret = int(temp) if temp.is_integer() else temp
            return SucceededValidation, ret
        except (ValueError, TypeError):
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('number', value)


class String(Variable):
    def __int__(self, value):
        super().__init__('string', value)

    @staticmethod
    def validate(value):
        if len(value) == 0:
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('string', value)

        start = value[0]
        end = value[-1]
        quotes = ['\'', '"']

        if start not in quotes or end not in quotes or start != end:
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('string', value)

        return SucceededValidation, value[1:-1]


class Array(Variable):
    def __int__(self, value):
        super().__init__('array', value)

    @staticmethod
    def validate(value):
        if value == '[]' or value == []:
            return SucceededValidation, []

        if len(value) == 0:
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('array', value)

        if value[0] != '[' or value[-1] != ']':
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('array', value)

        array_elements = [i.strip() for i in value[1:-1].split(',')]

        if '' in array_elements:
            return FailedValidation, Error.EmptyValueRaiser(array_elements, 'array')

        final_array = []
        value = value.replace(' ', '', value.count(' '))[1:-1]

        i = 0
        while i < len(value):
            if value[i] not in [',', ':', '[', ']', '{', '}']:
                end = value.index(',', i) if ',' in value[i:] else len(value)
                final_array.append(value[i:end])
                i = end + 1

            elif value[i] == '[':
                try:
                    end = sorted(Variable.find_parens(value, '[', ']'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Array.validate(value[i:end+1])
                if calculated[0] is FailedValidation:
                    return calculated
                final_array.append(calculated[1])
                i = end + 1
                if i < len(value) and value[i] == ',':
                    i += 1

            elif value[i] == '{':
                try:
                    end = sorted(Variable.find_parens(value, '{', '}'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Map.validate(value[i:end+1])
                if calculated[0] is FailedValidation:
                    return calculated
                final_array.append(calculated[1])
                i = end + 1
                if i < len(value) and value[i] == ',':
                    i += 1

            else:
                return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

        for i in range(len(final_array)):
            if type(final_array[i]) is str:
                el = type_of_variable(final_array[i])
                if len(el) == 0:
                    return FailedValidation, el[0]
                final_array[i] = el[1]

        return SucceededValidation, final_array


class Map(Variable):
    def __int__(self, value):
        super().__init__('mpa', value)

    @staticmethod
    def divide_to_pairs(value):
        if value == '':
            return []

        if not any(i in value for i in '{}[]()'):
            return [[j.strip() for j in i] for i in [i.split(':') for i in [i.strip() for i in value.split(',')]]]

        if '(' in value and ')' in value and not any(i in value for i in '{}[]'):
            start = value.index('(')
            end = len(value) - 1 - [value[i] for i in range(len(value) - 1, -1, -1)].index(')')
            result = Interpreter.Interpreter.run_single_command(value[start + 1:end])
            if result[0] is SucceededValidation:
                return Map.divide_to_pairs(value[:start] + result[1] + value[end + 1:])
            raise result[1]

        if '[' in value and ']' in value and not any(i in value for i in '{}') and value.count:
            value = value.replace(' ', '', value.count(' '))
            start, end = Map.find_parens(value, '[', ']')[0]
            arr = Array.validate('[' + value[start+1:end] + ']')
            if arr[0] is SucceededValidation:
                last_comma_before = value[:start].rfind(',')
                first_comma_after = value.find(',', end)
                divider = value.find(':', last_comma_before, start)

                if divider == -1:
                    if ':' in value:
                        divider = value.index(':')
                    else:
                        raise Error.EmptyValueRaiser(value, 'map-value')

                before = Map.divide_to_pairs(value[:last_comma_before+1][:-1])
                after = Map.divide_to_pairs(value[first_comma_after+1:]) if first_comma_after > -1 else []

                key = value[last_comma_before+1:divider]
                v = value[divider+1:first_comma_after] + (value[first_comma_after] if first_comma_after == -1 else '')

                if value[divider+1] == '[' and \
                        (value[first_comma_after-1] == ']' or (first_comma_after == -1 and value[-1] != ']')):
                    v = [SucceededValidation, v]
                else:
                    v = Interpreter.Interpreter.run_single_command(v)
                    if v[0] is FailedValidation:
                        raise v[1]

                return before + [[key, v[1]]] + after

            raise arr[1]

        if '{' in value and '}' in value:
            return []

    @staticmethod
    def validate(value):
        if value == '{}' or value == {}:
            return SucceededValidation, {}

        if len(value) == 0:
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('map', value)

        if value[0] != '{' or value[-1] != '}':
            return FailedValidation, Error.IdentifierDoesntMatchValueRaiser('map', value)

        elements = value[1:-1]
        elements_split_by_comma = [i.strip() for i in elements.split(',')]

        if elements == '':
            return SucceededValidation, {}

        if '' in elements_split_by_comma:
            return FailedValidation, Error.EmptyValueRaiser(elements_split_by_comma, 'map')

        final_map = []
        value = value.replace(' ', '', value.count(' '))[1:-1]
        writing_to_key = True
        key = ''

        i = 0
        while i < len(value):
            if value[i] not in [',', ':', '[', ']', '{', '}']:
                if ':' not in value[i:] and writing_to_key:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                if writing_to_key:
                    end = value.index(':', i)
                    key = value[i:end]

                    check_key = Variable.check_name(key)

                    if check_key[0] is FailedValidation:
                        return check_key

                    i = end + 1
                    writing_to_key = False
                else:
                    end = value.index(',', i) if ',' in value[i:] else len(value)
                    final_map.append([key, value[i:end]])
                    i = end + 1
                    writing_to_key = True
                    key = ''

            elif value[i] == '[' and not writing_to_key:
                try:
                    end = sorted(Variable.find_parens(value, '[', ']'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Array.validate(value[i:end+1])
                if calculated[0] is FailedValidation:
                    return calculated

                if not writing_to_key:
                    if key == '':
                        return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                    final_map.append([key, (str(calculated[1]) if (end + 1 < len(value) and value[end + 1] == ',')
                                            else calculated[1])])
                    key = ''
                    writing_to_key = False
                else:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                i = end + 1
                if i < len(value) and value[i] == ',':
                    writing_to_key = True
                    i += 1

            elif value[i] == '{' and not writing_to_key:
                try:
                    end = sorted(Variable.find_parens(value, '{', '}'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Map.validate(value[i:end+1])
                if calculated[0] is FailedValidation:
                    return calculated

                if not writing_to_key:
                    if key == '':
                        return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                    final_map.append([key, (str(calculated[1]) if (end + 1 < len(value) and value[end + 1] == ',')
                                            else calculated[1])])
                    key = ''
                    writing_to_key = False
                else:
                    return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                i = end + 1
                if i < len(value) and value[i] == ',':
                    writing_to_key = True
                    i += 1

            else:
                return FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

        for i in range(len(final_map)):
            if type(final_map[i][1]) is str:
                el = type_of_variable(final_map[i][1])
                if len(el) == 0:
                    return FailedValidation, el[0]
                final_map[i][1] = el[1]

        return SucceededValidation, dict(final_map)


class UnknownIdentifier(Variable):
    @staticmethod
    def validate(value):
        return FailedValidation, Error.UnknownIdentifierRaiser(value)


RESERVED_WORDS = [
    'boolean', 'number', 'string', 'array', 'map', 'node', 'stack', 'queue', 'tree', 'bstree', 'graph', 'delete_var',
    'typeof', 'print', 'input', 'if', 'else', 'while', 'for', 'from', 'to', 'skip', 'in', 'function', 'return', 'takes',
    'as',
]

VARIABLE_TYPES = {
    'null': Null,
    'boolean': Boolean,
    'number': Number,
    'string': String,
    'array': Array,
    'map': Map,
    # 'node': Node,
    # 'stack': Stack,
    # 'queue': Queue,
    # 'tree': Tree,
    # 'bstree': BSTree,
    # 'graph': Graph,
    'unknown': UnknownIdentifier
}

if __name__ == '__main__':
    print(type_of_variable('{a: 1, b:\'2\', c:[1, 2], d:[1,2]}'))
    print(Map.validate('{a: 1, b:\'2\', c:[x, 2], d:[1,2]}'))

    print(type_of_variable('{a: 1, b:\'2\', c:[1, 2], d:[[1], [2]]}'))

    print(type_of_variable('{a: 1, b:\'2\', x:{c:[1, 2], d:[1,2], e:{f:1, g:[2], h: {x:1}}}}'))
    print(type_of_variable('[1, \'2\', {a: [2, 3]}]'))
