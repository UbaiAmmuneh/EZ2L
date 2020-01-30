import re

import Error
from Interpreter import Interpreter
from Variables import type_of_variable, add_variable, delete_variable, variable_exists, get_variable, \
    Variable, Number, Boolean


def check_semicolon(keyword, command):
    if command[-1] != ';':
        raise Error.SemiColonMissingRaiser(keyword, command)


def find_operations(command):
    ops = []
    for op in OPERATIONS:
        if command.find(OPERATIONS[op].keyword) > -1:
            ops.append(OPERATIONS[op])

    return ops


class PrintOp:
    keyword = 'print'
    structure = r'print\s*\(\s*(.*?)\s*\)'
    power = -1

    @staticmethod
    def perform(command):
        match = re.findall(PrintOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'print(<output>)')

        match = match[0]

        output = Interpreter.run_single_command(match)

        if len(output) == 1:
            raise output[0]

        print(output[1])


class InputOp:
    keyword = 'input'
    structure = r'input'
    power = 10

    @staticmethod
    def perform(command):
        match = re.match(InputOp.structure, command)

        if match is None:
            raise Error.BadSyntaxRaiser(command, 'input')

        return input()


class VariableAssignmentOp:
    keyword = '='
    structure = r'(\w+)\s=\s*([^;]*);?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(VariableAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<var_name> = <value>')

        match = match[0]
        var_name = Variable.check_name(match[0])
        var_value = Interpreter.run_single_command(match[1], get_type_of_var=True)

        if var_name[0] is Error.FailedValidation:
            raise var_name[1]

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name[1], var_value[1][0], var_value[1][1])


class VariableDeletionOp:
    keyword = 'del'
    structure = r'del\s*(\w+)'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(VariableDeletionOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'del <var_name>')

        match = match[0]
        var_name = Variable.check_name(match[0])

        if var_name[0] is Error.FailedValidation:
            raise var_name[1]

        delete_variable(var_name[1])


class NumericAdditionOp:
    keyword = '+'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*\+\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 1

    @staticmethod
    def perform(command):
        match = re.findall(NumericAdditionOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> + <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('+', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('+', op2, 'number')

        return op1[1] + op2[1]


class NumericSubtractionOp:
    keyword = '-'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[-]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 1

    @staticmethod
    def perform(command):
        match = re.findall(NumericSubtractionOp.structure, command)

        if len(match) == 0:
            _ = re.match(r'.*?([-][0-9]+)[)\s]*;?$', command)
            if _ is not None:
                return type_of_variable(_.groups()[0])[1]

            raise Error.BadSyntaxRaiser(command, '<operator1> - <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('-', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('-', op2, 'number')

        return op1[1] - op2[1]


class NumericMultiplicationOp:
    keyword = '*'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[*]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

    @staticmethod
    def perform(command):
        match = re.findall(NumericMultiplicationOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> * <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('*', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('*', op2, 'number')

        return op1[1] * op2[1]


class NumericDivisionOp:
    keyword = '/'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[/]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

    @staticmethod
    def perform(command):
        match = re.findall(NumericDivisionOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> / <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('/', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('/', op2, 'number')

        return op1[1] / op2[1]


class NumericModuloOp:
    keyword = '%'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[%]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

    @staticmethod
    def perform(command):
        match = re.findall(NumericModuloOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> % <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('%', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('%', op2, 'number')

        return op1[1] % op2[1]


class NumericPowerOp:
    keyword = '**'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[*][*]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 3

    @staticmethod
    def perform(command):
        match = re.findall(NumericPowerOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> ** <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('**', op1, 'number')

        if not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('**', op2, 'number')

        return op1[1] ** op2[1]


class NumericAdditionAssignmentOp:
    keyword = 'add'
    structure = r'\s*add\s*([0-9a-zA-Z._\-]+)\s+to\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericAdditionAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'add <value> to <var_name>')

        match = match[0]
        var_name = match[1]
        var_value = Interpreter.run_single_command(match[0], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[0])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], var_value[1][1] + get_variable(var_name)['value'])


class NumericSubtractionAssignmentOp:
    keyword = 'subtract'
    structure = r'\s*subtract\s*([0-9a-zA-Z._\-]+)\s+from\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericSubtractionAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'subtract <value> from <var_name>')

        match = match[0]
        var_name = match[1]
        var_value = Interpreter.run_single_command(match[0], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[0])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], get_variable(var_name)['value'] - var_value[1][1])


class NumericMultiplicationAssignmentOp:
    keyword = 'multiply'
    structure = r'\s*multiply\s*([0-9a-zA-Z._\-]+)\s+by\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericMultiplicationAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'multiply <var_name> by <value>')

        match = match[0]
        var_name = match[0]
        var_value = Interpreter.run_single_command(match[1], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[1])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], get_variable(var_name)['value'] * var_value[1][1])


class NumericDivisionAssignmentOp:
    keyword = 'divide'
    structure = r'\s*divide\s*([0-9a-zA-Z._\-]+)\s+by\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericDivisionAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'divide <var_name> by <value>')

        match = match[0]
        var_name = match[0]
        var_value = Interpreter.run_single_command(match[1], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[1])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], get_variable(var_name)['value'] / var_value[1][1])


class NumericPowerAssignmentOp:
    keyword = 'raise'
    structure = r'\s*raise\s*([0-9a-zA-Z._\-]+)\s+to power\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericPowerAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'raise <var_name> to power <value>')

        match = match[0]
        var_name = match[0]
        var_value = Interpreter.run_single_command(match[1], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[1])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], get_variable(var_name)['value'] ** var_value[1][1])


class NumericModuloAssignmentOp:
    keyword = 'modulo'
    structure = r'\s*modulo\s*([0-9a-zA-Z._\-]+)\s+by\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 0

    @staticmethod
    def perform(command):
        match = re.findall(NumericModuloAssignmentOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'modulo <var_name> by <value>')

        match = match[0]
        var_name = match[0]
        var_value = Interpreter.run_single_command(match[1], get_type_of_var=True)

        if not variable_exists(var_name):
            raise Error.VariableNotFoundRaiser(match[1])

        if var_value[0] is Error.FailedValidation:
            raise var_value[1][0]

        add_variable(var_name, var_value[1][0], get_variable(var_name)['value'] % var_value[1][1])


class BooleanAndOp:
    keyword = 'and'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*and\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 3

    @staticmethod
    def perform(command):
        match = re.findall(BooleanAndOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> and <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('and', op1, 'boolean')

        if not op2[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('and', op2, 'boolean')

        return op1[1] and op2[1]


class BooleanOrOp:
    keyword = 'or'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*or\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 1

    @staticmethod
    def perform(command):
        match = re.findall(BooleanOrOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> or <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('or', op1, 'boolean')

        if not op2[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('and', op2, 'boolean')

        return op1[1] or op2[1]


class BooleanXorOp:
    keyword = 'xor'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*xor\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

    @staticmethod
    def perform(command):
        match = re.findall(BooleanXorOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> xor <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('xor', op1, 'boolean')

        if not op2[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('xor', op2, 'boolean')

        return op1[1] ^ op2[1]


class BooleanNotOp:
    keyword = 'not'
    structure = r'\s*not\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 4

    @staticmethod
    def perform(command):
        match = re.findall(BooleanNotOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, 'not <operator>')

        op = type_of_variable(match[0])

        if len(op) == 1:
            raise op[0]

        if not op[0] is Boolean:
            raise Error.WrongOperationArgumentTypeRaiser('not', op, 'boolean')

        return not op[1]


class BitwiseAndOp:
    keyword = '&'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[&]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 3

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseAndOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> & <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean and not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('&', op1, 'number / boolean')

        if not op2[0] is Boolean and not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('&', op2, 'number / boolean')

        return op1[1] & op2[1]


class BitwiseOrOp:
    keyword = '|'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*[|]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 1

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseOrOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> | <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean and not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('|', op1, 'number / boolean')

        if not op2[0] is Boolean and not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('|', op2, 'number / boolean')

        return op1[1] | op2[1]


class BitwiseXorOp:
    keyword = '^'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*\^\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseXorOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> ^ <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean and not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('^', op1, 'number / boolean')

        if not op2[0] is Boolean and not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('^', op2, 'number / boolean')

        return op1[1] ^ op2[1]


class BitwiseRightShiftOp:
    keyword = '>>'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*>>\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 4

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseRightShiftOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> >> <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean and not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('>>', op1, 'number / boolean')

        if not op2[0] is Boolean and not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('>>', op2, 'number / boolean')

        return op1[1] >> op2[1]


class BitwiseLeftShiftOp:
    keyword = '<<'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*<<\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 4

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseLeftShiftOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '<operator1> << <operator2>')

        match = match[0]
        op1 = type_of_variable(match[0])
        op2 = type_of_variable(match[1])

        if len(op1) == 1:
            raise op1[0]

        if len(op2) == 1:
            raise op2[0]

        if not op1[0] is Boolean and not op1[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('<<', op1, 'number / boolean')

        if not op2[0] is Boolean and not op2[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('<<', op2, 'number / boolean')

        return op1[1] << op2[1]


class BitwiseNotOp:
    keyword = '!'
    structure = r'\s*[!]\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 5

    @staticmethod
    def perform(command):
        match = re.findall(BitwiseNotOp.structure, command)

        if len(match) == 0:
            raise Error.BadSyntaxRaiser(command, '! <operator>')

        op = type_of_variable(match[0])

        if len(op) == 1:
            raise op[0]

        if not op[0] is Boolean and not op[0] is Number:
            raise Error.WrongOperationArgumentTypeRaiser('!', op, 'boolean / number')

        return ~ op[1]


OPERATIONS = {
    'print': PrintOp,
    'input': InputOp,
    '=': VariableAssignmentOp,
    'del': VariableDeletionOp,
    '+': NumericAdditionOp,
    '-': NumericSubtractionOp,
    '*': NumericMultiplicationOp,
    '/': NumericDivisionOp,
    '%': NumericModuloOp,
    '**': NumericPowerOp,
    'and': BooleanAndOp,
    'or': BooleanOrOp,
    'xor': BooleanXorOp,
    'not': BooleanNotOp,
    '&': BitwiseAndOp,
    '|': BitwiseOrOp,
    '^': BitwiseXorOp,
    '>>': BitwiseRightShiftOp,
    '<<': BitwiseLeftShiftOp,
    '!': BitwiseNotOp,
    'add': NumericAdditionAssignmentOp,
    'subtract': NumericSubtractionAssignmentOp,
    'multiply': NumericMultiplicationAssignmentOp,
    'divide': NumericDivisionAssignmentOp,
    'raise': NumericPowerAssignmentOp,
    'modulo': NumericModuloAssignmentOp
}

# ** > *, /, % > +, -
# not > and > xor > or
# ! > shift left, shift right > & > ^ > |
