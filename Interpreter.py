from Error import SucceededValidation, FailedValidation
import Operations
from PrimitiveDataStructures import Variable


class Interpreter:
    def __init__(self):
        pass

    @staticmethod
    def run_single_command(command):
        if '(' in command:
            start, end = Variable.find_parens(command, '(', ')')[0]
            inner = Interpreter.run_single_command(command[start + 1:end])
            if inner[0] is FailedValidation:
                raise inner[1]
            return Interpreter.run_single_command(command[:start] + inner[1] + command[end + 1:])

        result = Operations.Operation.perform(command)
        if result[0] is SucceededValidation:
            if result[1] is not None:
                print(result[1])
        else:
            raise result[1]

    @staticmethod
    def run_function(function_body):
        pass

    @staticmethod
    def declare_class(class_body):
        pass

    @staticmethod
    def run(program):
        pass


if __name__ == '__main__':
    interpreter = Interpreter()
    pass
