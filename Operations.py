import re

import Error
from Variables import type_of_variable


def check_semicolon(keyword, command):
    if command[-1] != ';':
        raise Error.SemiColonMissingRaiser(keyword, command)


class PrintOp:
    keyword = 'print'
    structure = r'print\((.*)\)\s*'

    @staticmethod
    def perform(command):
        match = re.match(PrintOp.structure, command)

        if match is None:
            check_semicolon(PrintOp.keyword, command)
            raise Error.BadSyntaxRaiser(command, 'print(<output>)')

        output = type_of_variable(match.groups()[0])

        if len(output) == 1:
            raise output[0]

        print(output[1])


class InputOp:
    keyword = 'input'
    structure = r'input\s*'

    @staticmethod
    def perform(command):
        match = re.match(InputOp.structure, command)

        if match is None:
            check_semicolon(InputOp.keyword, command)
            raise Error.BadSyntaxRaiser(command, 'input')

        return input()


def find_operation(command):
    par = command if ' ' not in command else command[:command.index(' ')]
    for op in OPERATIONS:
        if par.find(OPERATIONS[op].keyword) > -1:
            return OPERATIONS[op],

    return None, par


OPERATIONS = {
    'print': PrintOp,
    'input': InputOp,
}
