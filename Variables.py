import re

import Error


def load_variables():
    pass


def variable_exists(var_name):
    load_variables()
    return var_name.__hash__ is not None and var_name in VARIABLES


def add_variable(var_name, var_type, var_value):
    VARIABLES[var_name] = {'class_name': var_type, 'value': var_value}


def get_variable(var_name):
    if variable_exists(var_name):
        return VARIABLES.get(var_name, None)

    return Error.VariableNotFoundRaiser(var_name)


def delete_variable(var_name):
    if variable_exists(var_name):
        del VARIABLES[var_name]

    return Error.VariableNotFoundRaiser(var_name)


def type_of_variable(var, check_variables=True):
    if var in RESERVED_WORDS:
        return [Error.UsageOfReservedWordRaiser(var)]

    for _ in VARIABLE_TYPES:
        variable_type = VARIABLE_TYPES.get(_)
        if var is None:
            return [Error.UnknownIdentifierRaiser(var)]
        if var is not None and variable_type.simple_validate(_, var):
            temp = variable_type.validate(var)
            if temp[0] is Error.SucceededValidation:
                return [variable_type, temp[1]]
    if check_variables:
        if variable_exists(var):
            variable = get_variable(var)
            return [variable.get('class_name'), variable.get('value')]
    return [Error.UnknownIdentifierRaiser(var)]


class Variable:
    def __init__(self, var_type, value):
        self.var_type = var_type
        self.value = VARIABLE_TYPES.get(self.var_type)(value)

    def __repr__(self):
        return self.value

    @staticmethod
    def check_name(name):
        if re.match(r'[a-zA-Z_]\w*', name):
            return Error.SucceededValidation, name
        return Error.FailedValidation, Error.BadVariableNameRaiser(name)

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
            print(pstack, toret)
            raise IndexError("No matching opening parens at: " + str(pstack.pop()))

        return toret

    @staticmethod
    def simple_validate(var_type, value):
        return VARIABLE_TYPES.get(var_type).validate(value)[0] is Error.SucceededValidation


class Null(Variable):
    keyword = 'Null'

    def __init__(self, value):
        super().__init__('null', value)

    @staticmethod
    def validate(value):
        if value == 'null' or value == 'None':
            return Error.SucceededValidation, None
        return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('null', value)


class Boolean(Variable):
    keyword = 'Boolean'

    def __int__(self, value):
        super().__init__('boolean', value)

    @staticmethod
    def validate(value):
        values = {'true': True, 'false': False, 'True': True, 'False': False}
        if value.__hash__ is not None and value in values:
            return Error.SucceededValidation, values.get(value)
        return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('boolean', value)


class Number(Variable):
    keyword = 'Number'

    def __int__(self, value):
        super().__init__('number', value)

    @staticmethod
    def validate(value):
        try:
            temp = float(value)
            ret = int(temp) if temp.is_integer() else temp
            return Error.SucceededValidation, ret
        except (ValueError, TypeError):
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('number', value)


class String(Variable):
    keyword = 'String'

    def __int__(self, value):
        super().__init__('string', value)

    @staticmethod
    def validate(value):
        if len(value) == 0:
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('string', value)

        if value[0] == value[-1] and value[0] in ['\'', '"']:
            return Error.SucceededValidation, value[1:-1]

        return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('string', value)


class Array(Variable):
    keyword = 'Array'

    def __int__(self, value):
        super().__init__('array', value)

    @staticmethod
    def simple_validate(var_type, value):
        return len(value) > 0 and value[0] == '[' and value[-1] == ']'

    @staticmethod
    def validate(value):
        if value == '[]' or value == []:
            return Error.SucceededValidation, []

        if len(value) == 0:
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('array', value)

        if value[0] != '[' or value[-1] != ']':
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('array', value)

        array_elements = [i.strip() for i in value[1:-1].split(',')]

        if '' in array_elements:
            return Error.FailedValidation, Error.EmptyValueRaiser(array_elements, 'array')

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
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Array.validate(value[i:end + 1])
                if calculated[0] is Error.FailedValidation:
                    return calculated
                final_array.append(calculated[1])
                i = end + 1
                if i < len(value) and value[i] == ',':
                    i += 1

            elif value[i] == '{':
                try:
                    end = sorted(Variable.find_parens(value, '{', '}'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Map.validate(value[i:end + 1])
                if calculated[0] is Error.FailedValidation:
                    return calculated
                final_array.append(calculated[1])
                i = end + 1
                if i < len(value) and value[i] == ',':
                    i += 1

            else:
                return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

        for i in range(len(final_array)):
            if type(final_array[i]) is str:
                el = type_of_variable(final_array[i])
                if len(el) == 0:
                    return Error.FailedValidation, el[0]
                final_array[i] = el[1]

        return Error.SucceededValidation, final_array


class Map(Variable):
    keyword = 'Map'

    def __int__(self, value):
        super().__init__('mpa', value)

    @staticmethod
    def simple_validate(var_type, value):
        return value[0] == '{' and value[-1] == '}'

    @staticmethod
    def divide_to_pairs(value):
        from Operations import run_command

        if value == '':
            return []

        if not any(i in value for i in '{}[]()'):
            return [[j.strip() for j in i] for i in [i.split(':') for i in [i.strip() for i in value.split(',')]]]

        if '(' in value and ')' in value and not any(i in value for i in '{}[]'):
            start = value.index('(')
            end = len(value) - 1 - [value[i] for i in range(len(value) - 1, -1, -1)].index(')')
            result = run_command(value[start + 1:end])
            if result[0] is Error.SucceededValidation:
                return Map.divide_to_pairs(value[:start] + result[1] + value[end + 1:])
            raise result[1]

        if '[' in value and ']' in value and not any(i in value for i in '{}') and value.count:
            value = value.replace(' ', '', value.count(' '))
            start, end = Map.find_parens(value, '[', ']')[0]
            arr = Array.validate('[' + value[start + 1:end] + ']')
            if arr[0] is Error.SucceededValidation:
                last_comma_before = value[:start].rfind(',')
                first_comma_after = value.find(',', end)
                divider = value.find(':', last_comma_before, start)

                if divider == -1:
                    if ':' in value:
                        divider = value.index(':')
                    else:
                        raise Error.EmptyValueRaiser(value, 'map-value')

                before = Map.divide_to_pairs(value[:last_comma_before + 1][:-1])
                after = Map.divide_to_pairs(value[first_comma_after + 1:]) if first_comma_after > -1 else []

                key = value[last_comma_before + 1:divider]
                v = value[divider + 1:first_comma_after] + (value[first_comma_after] if first_comma_after == -1 else '')

                if value[divider + 1] == '[' and \
                        (value[first_comma_after - 1] == ']' or (first_comma_after == -1 and value[-1] != ']')):
                    v = [Error.SucceededValidation, v]
                else:
                    v = run_command(v)
                    if v[0] is Error.FailedValidation:
                        raise v[1]

                return before + [[key, v[1]]] + after

            raise arr[1]

        if '{' in value and '}' in value:
            return []

    @staticmethod
    def validate(value):
        if value == '{}' or value == {}:
            return Error.SucceededValidation, {}

        if len(value) == 0:
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('map', value)

        if value[0] != '{' or value[-1] != '}':
            return Error.FailedValidation, Error.IdentifierDoesntMatchValueRaiser('map', value)

        elements = value[1:-1]
        elements_split_by_comma = [i.strip() for i in elements.split(',')]

        if elements == '':
            return Error.SucceededValidation, {}

        if '' in elements_split_by_comma:
            return Error.FailedValidation, Error.EmptyValueRaiser(elements_split_by_comma, 'map')

        final_map = []
        value = value.replace(' ', '', value.count(' '))[1:-1]
        writing_to_key = True
        key = ''

        i = 0
        while i < len(value):
            if value[i] not in [',', ':', '[', ']', '{', '}']:
                if ':' not in value[i:] and writing_to_key:
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                if writing_to_key:
                    end = value.index(':', i)
                    key = value[i:end]

                    check_key = Variable.check_name(key)

                    if check_key[0] is Error.FailedValidation:
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
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Array.validate(value[i:end + 1])
                if calculated[0] is Error.FailedValidation:
                    return calculated

                if not writing_to_key:
                    if key == '':
                        return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                    final_map.append([key, (str(calculated[1]) if (end + 1 < len(value) and value[end + 1] == ',')
                                            else calculated[1])])
                    key = ''
                    writing_to_key = False
                else:
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                i = end + 1
                if i < len(value) and value[i] == ',':
                    writing_to_key = True
                    i += 1

            elif value[i] == '{' and not writing_to_key:
                try:
                    end = sorted(Variable.find_parens(value, '{', '}'), key=lambda j: j[0] == i, reverse=True)[0][1]
                except IndexError:
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                calculated = Map.validate(value[i:end + 1])
                if calculated[0] is Error.FailedValidation:
                    return calculated

                if not writing_to_key:
                    if key == '':
                        return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                    final_map.append([key, (str(calculated[1]) if (end + 1 < len(value) and value[end + 1] == ',')
                                            else calculated[1])])
                    key = ''
                    writing_to_key = False
                else:
                    return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

                i = end + 1
                if i < len(value) and value[i] == ',':
                    writing_to_key = True
                    i += 1

            else:
                return Error.FailedValidation, Error.InvalidKeyValuePairStructureRaiser(value)

        for i in range(len(final_map)):
            if type(final_map[i][1]) is str:
                el = type_of_variable(final_map[i][1])
                if len(el) == 0:
                    return Error.FailedValidation, el[0]
                final_map[i][1] = el[1]

        # noinspection PyTypeChecker
        return Error.SucceededValidation, dict(final_map)


class BinarySearchTree:
    def __init__(self, value):
        self.__value = value
        self.__left_child = None
        self.__right_child = None
        self.__parent = None

    def __repr__(self):
        return '\n'.join(self.display())

    def get_value(self):
        return self.__value

    def get_left(self):
        return self.__left_child

    def get_right(self):
        return self.__right_child

    def get_parent(self):
        return self.__parent

    def set_value(self, value):
        self.__value = value

    def set_left(self, left):
        self.__left_child = left
        if type(left) is BinarySearchTree:
            left.set_parent(self)

    def set_right(self, right):
        self.__right_child = right
        if type(right) is BinarySearchTree:
            right.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def has_value(self):
        return self.get_value() is not None

    def has_left(self):
        return self.get_left() is not None

    def has_right(self):
        return self.get_right() is not None

    def has_parent(self):
        return self.get_parent() is not None

    def is_empty(self):
        return not self.has_value() and self.is_leaf()

    def is_leaf(self):
        return not self.has_right() and not self.has_left()

    def min_value(self):
        current = self

        while current.has_left():
            current = current.get_left()

        return current.get_value()

    def max_value(self):
        current = self

        while current.has_right():
            current = current.get_right()

        return current.get_value()

    def search(self, value):
        try:
            if self.get_value() == value:
                return self
            elif self.get_value() > value:
                return self.get_left().search(value) if self.has_left() else None
            else:
                return self.get_right().search(value) if self.has_right else None
        except TypeError:
            raise Error.IncomparableItemsRaiser(value)

    def insert(self, value):
        try:
            if self.is_leaf() and not self.has_value():
                self.set_value(value)
                return self

            if self.get_value() > value:
                if not self.has_left():
                    self.set_left(BinarySearchTree(value))
                    return self.get_left()
                else:
                    return self.get_left().insert(value)
            elif self.get_value() < value:
                if not self.has_right():
                    self.set_right(BinarySearchTree(value))
                    return self.get_right()
                else:
                    return self.get_right().insert(value)
        except TypeError:
            raise Error.IncomparableItemsRaiser(value)

    def remove(self, value):
        if value is None:
            return

        node = self.search(value)

        if node.has_parent():
            parent = node.get_parent()

            if node.is_leaf():
                if parent.get_left() == node:
                    parent.set_left(None)
                else:
                    parent.set_right(None)

            else:
                if node.has_right() and node.has_left():
                    left = node.get_left()
                    parent.set_right(node.get_right())
                    temp = parent.get_right()
                    while temp.has_left():
                        temp = temp.get_left()
                    temp.set_left(left)

                elif not node.has_left():
                    parent.set_right(node.get_right())

                else:
                    parent.set_right(node.get_left())

            return self

        else:
            if node.is_leaf():
                return None

            if not node.has_right():
                return node.get_left()

            if not node.has_left():
                return node.get_right()

            left = node.get_left()
            right = node.get_right()
            temp = right

            while temp.has_left():
                temp = temp.get_left()

            temp.set_left(left)

            return right

    def get_all_nodes(self):
        return self.get_left().get_all_nodes() \
            if self.has_left() \
            else [] + [self.get_value()] + self.get_right().get_all_nodes() if self.has_right() else []

    def _balance(self, nodes, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        node = nodes[mid]

        node.set_left(self._balance(nodes, start, mid - 1))
        node.set_right(self._balance(nodes, mid + 1, end))

        return node

    def balance(self):
        nodes = self.get_all_nodes()
        return self._balance(nodes, 0, len(nodes) - 1)

    def depth(self):
        if self.is_leaf():
            return 1
        return 1 + max(self.get_left().depth() if self.has_left() else 0,
                       self.get_right().depth() if self.has_right() else 0)

    def find_max_node_length(self):
        return max(len(str(self.get_value())),
                   self.get_left().find_max_node_length() if self.has_left() else -1,
                   self.get_right().find_max_node_length() if self.has_right() else -1)

    def values_in_level(self, level):
        if level == 0:
            return [str(self.get_value())]

        return (self.get_left().values_in_level(level - 1) if self.has_left() else [''] * (2 ** (level - 1))) + \
               (self.get_right().values_in_level(level - 1) if self.has_right() else [''] * (2 ** (level - 1)))

    def display(self):
        lines = []
        node_width = self.find_max_node_length()
        node_width += ((node_width + 1) % 2)
        depth = self.depth()
        line_width = (2 ** depth - 1) * node_width
        spacer1 = (line_width - node_width) // (2 * node_width)
        space1 = ' ' * node_width * spacer1

        left_corner = (' ' * (node_width - 1) + '_')
        right_corner = ('_' + ' ' * (node_width - 1))
        middle_spacer = (' ' * ((node_width - 1) // 2) + '|' + ' ' * ((node_width - 1) // 2))
        _ = '_' * node_width

        for level in range(depth):
            spacer2 = 2 * spacer1 + 1
            space2 = ' ' * node_width * spacer2
            line1 = ''
            line2 = space1
            line3 = space1
            values = [('{:^%s.%s}' % (node_width, node_width)).format(j) for j in self.values_in_level(level)]
            for i in range(len(values)):
                if i < len(values) // 2:
                    cond1 = len(values[i * 2].strip()) > 0
                    cond2 = len(values[i * 2 + 1].strip()) > 0
                    left = (left_corner + _ * spacer1 if cond1 else ' ' * (node_width + node_width * spacer1))
                    right = (_ * spacer1 + right_corner if cond2 else ' ' * (node_width + node_width * spacer1))
                    middle = (('_' if cond1 else ' ') * ((node_width - 1) // 2) +
                              ('|' if (cond1 or cond2) else ' ') +
                              ('_' if cond2 else ' ') * ((node_width - 1) // 2))
                    ___ = left + middle + right
                    line1 += (space1 + ___ + space1 + ' ' * node_width)

                line2 += (middle_spacer if len(values[i].strip()) > 0 else ' ' * node_width) + space2
                line3 += values[i] + space2

            if level > 0:
                lines.append(line1)
                lines.append(line2)
            lines.append(line3)
            spacer1 = (spacer1 - 1) // 2
            space1 = ' ' * node_width * spacer1

        return lines


class LinkedList:
    def __init__(self, value):
        self.__value = value
        self.__next = None
        self.__prev = None

    def __repr__(self):
        return ''.join(self.display())

    def get_value(self):
        return self.__value

    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_value(self, value):
        self.__value = value

    def set_next(self, next_):
        self.__next = next_

        if next_ is not None:
            next_.set_prev(self)

    def set_prev(self, prev):
        self.__prev = prev

    def is_empty(self):
        return self.get_value() is None and self.get_next() is None

    def insert_at_head(self, value):
        old_value = self.get_value()
        old_next = self.get_next()
        self.set_value(value)
        self.set_next(LinkedList(old_value))
        self.get_next().set_next(old_next)

    def insert_at_end(self, value):
        temp = self

        while temp.get_next() is not None:
            temp = temp.get_next()

        temp.set_next(LinkedList(value))

    def search(self, value):
        temp = self

        while temp is not None:
            if temp.get_value() == value:
                break
            temp = temp.get_next()

        return temp

    def delete(self, value):
        node = self.search(value)

        if node.get_prev() is not None:
            node.get_prev().set_next(node.get_next())
        else:
            self.set_value(self.get_next().get_value())
            self.set_next(self.get_next().get_next())

    def display(self):
        temp = self
        lines = []

        while temp.get_next() is not None:
            lines.append(str(temp.get_value()) + ' <--> ')
            temp = temp.get_next()

        lines.append(temp.get_value())

        return lines


class Stack:
    def __init__(self):
        self.values = []

    def __repr__(self):
        return '\n'.join(self.display())

    def top(self):
        return self.values[-1]

    def push(self, value):
        self.values.append(value)

    def pop(self):
        try:
            return self.values.pop()
        except IndexError:
            pass

    def is_empty(self):
        return len(self.values) == 0

    def reverse(self):
        _reversed = Stack()

        while not self.is_empty():
            _reversed.push(self.pop())

        self.values = _reversed.values

    def display(self):
        lines = []

        if len(self.values) > 0:
            max_node_length = max(len(str(i)) for i in self.values)
            top_line = ' %s ' % ('_' * (max_node_length + 2))
            bottom_line = top_line.replace('_', '͞')
            lines.append(top_line)
            for i in range(len(self.values)):
                value = self.values[-i - 1]
                line = ('| {:^%s.%s} |' % (max_node_length, max_node_length)).format(str(value))
                lines.append(line + (' <- Top' if i == 0 else ''))
            lines.append(bottom_line)
        else:
            lines.append(' __ \n|  |\n ͞͞ \n')

        return lines


class RedBlackTree:
    pass


class AVLTree:
    pass


class WAVLTree:
    pass


class MaxHeap:
    pass


class Graph:
    pass


VARIABLE_TYPES = {
    'null': Null,
    'boolean': Boolean,
    'number': Number,
    'string': String,
    'array': Array,
    'map': Map,
}

# from Operations import OPERATIONS

RESERVED_WORDS = list(VARIABLE_TYPES.keys()) # + list(OPERATIONS.keys())

VARIABLES = {}

print(type_of_variable('[1, [], 2, 1 + 2 , \'hello there\', true, null, [{}, [], [1, 2, 3, [{a: 1}]]]]'))
