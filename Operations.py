import re

import Error
from Variables import type_of_variable, Variable, add_variable, delete_variable, Number, Boolean
from Interpreter import Interpreter


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
    power = 0

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


class BooleanAndOp:
    keyword = 'and'
    structure = r'\s*([0-9a-zA-Z._\-]+)\s*and\s*([\d0-9a-zA-Z._]+)\s*?'
    power = 2

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
    'and': BooleanAndOp
}
