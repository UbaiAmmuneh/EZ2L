from Error import SucceededValidation, FailedValidation, UnknownOperationRaiser


class Interpreter:
    def __init__(self):
        pass

    @staticmethod
    def run_single_command(command, check_for_semi_colon=False):
        from Variables import type_of_variable, Variable
        from Operations import find_operation, check_semicolon

        check = type_of_variable(command)
        if len(check) > 1:
            return SucceededValidation, check[1]

        op = find_operation(command)

        if check_for_semi_colon:
            check_semicolon(op[0].keyword, command)

        if '(' in command:
            start, end = Variable.find_parens(command, '(', ')')[-1]
            inner = Interpreter.run_single_command(command[start + 1:end])
            if inner[0] is FailedValidation:
                raise inner[1]

            res = (inner[1] if type(inner[1]) is not str else "'%s'" % inner[1])

            if len(op) > 1 or op[0].keyword not in ['print']:
                return Interpreter.run_single_command(command[:start] + res + command[end + 1:])

            command = command[:start + 1] + str(res) + command[end:]

        if len(op) > 1:
            raise UnknownOperationRaiser(op)

        result = op[0].perform(command)
        return SucceededValidation, ('' if result is None else result)

    @staticmethod
    def run_function(function_body):
        pass

    @staticmethod
    def declare_class(class_body):
        pass

    @staticmethod
    def run_code_block(program):
        pass


if __name__ == '__main__':
    Interpreter.run_single_command("print(input);", True)
