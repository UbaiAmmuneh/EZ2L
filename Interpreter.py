import re

from Error import SucceededValidation, FailedValidation, UnknownOperationRaiser


class Interpreter:
    def __init__(self):
        pass

    @staticmethod
    def run_single_command(command, check_for_semi_colon=False, get_type_of_var=False):
        from Variables import type_of_variable, Variable, String
        from Operations import find_operations, check_semicolon

        check = type_of_variable(command)
        if get_type_of_var:
            return SucceededValidation if len(check) > 1 else FailedValidation, check
        if len(check) > 1:
            return SucceededValidation, check[1]

        ops = sorted(find_operations(command), key=lambda x: -x.power)
        if check_for_semi_colon:
            check_semicolon(ops[0].keyword, command)

        if '(' in command:
            start, end = Variable.find_parens(command, '(', ')')[-1]
            inner = Interpreter.run_single_command(command[start + 1:end])

            if inner[0] is FailedValidation:
                raise inner[1]

            res = str(inner[1]) if type_of_variable(inner[1])[0] is not String else "'%s'" % inner[1]

            if len(ops) == 0 or 'print' not in [i.keyword for i in ops]:
                return Interpreter.run_single_command(command[:start] + res + command[end + 1:])

            command = command[:start + 1] + '%s' % res + command[end:]

        if len(ops) == 0:
            raise UnknownOperationRaiser(command)

        f = False

        while len(ops) > 0:
            if len(type_of_variable(command)) > 1:
                ops = ops[1:]
                continue

            ops = sorted(find_operations(command), key=lambda x: -x.power)

            if len(ops) == 0:
                break

            if f:
                ops = ops[1:]
                f = False

            op = ops[0]

            _ = op.perform(command)
            _ = str(_) if type_of_variable(_)[0] is not String else "'%s'" % _
            _s = re.search(op.structure, command)
            if _s is not None:
                s = _s.span()
            elif op.keyword == '-':
                s = re.search(r'([-][0-9]+)', command).span()
                f = True
            else:
                raise Exception('Unexpected Error')
            command = command.replace(command[s[0]:s[1]], _ if _ is not None else '')

        return SucceededValidation, command

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
    pass
    # Interpreter.run_single_command("print(1 + 2 + x);", True)
    # Interpreter.run_single_command("print(1 * 2 * x);", True)
    # Interpreter.run_single_command("print(1 - 2 - x);", True)
    # Interpreter.run_single_command("print(1 / 2 / x / 2);", True)
    # Interpreter.run_single_command("print(15% 6%2);", True)
    # Interpreter.run_single_command("print(-2);", True)
    # Interpreter.run_single_command("print(-2 + 1 * 3);", True)
    # Interpreter.run_single_command("print(15% 6%2);", True)

    #
    #
    #
    # Interpreter.run_single_command("x = true;", True)
    # Interpreter.run_single_command("print(x);", True)
    # Interpreter.run_single_command("print(true);", True)

    # Interpreter.run_single_command("print(1 + 2 - 3);", True)

    # x = """
    # x =1;
    # y  = 2;
    # del x;
    # print(y);
    #
    # if(x > 0) {
    # 	DOSOMETHING;
    # }
    # else if {
    # 	BBB;
    # 	CCC;
    # } else
    # {
    # 	DDDD;
    # 	V
    # 	;
    # 	V
    # 	;
    # }
    #
    # vvvv;
    # for i in 1{
    # 	weofnweofn
    # 	{}
    # 	woeifnweofni
    #
    # }
    #
    # while {} woicnewd {} {
    # 	qowendoewindoewd
    # 	}
    # oncoewncew;
    # """
    # from Variables import Variable
    #
    # print(Variable.find_parens(x, '{', '}'))
