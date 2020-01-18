from Variables import SucceededValidation, FailedValidation


class Interpreter:
    def __init__(self):
        pass

    @staticmethod
    def run_single_command(command):
        if '(' in command:
            start = command.index('(')
            end = len(command) - 1 - [command[i] for i in range(len(command) - 1, -1, -1)].index(')')
            return Interpreter.run_single_command(command[:start] +
                                                  Interpreter.run_single_command(command[start + 1:end]) +
                                                  command[end + 1:])

        return SucceededValidation, command

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
