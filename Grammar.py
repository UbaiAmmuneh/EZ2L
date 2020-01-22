"""
Conditions:
    Syntax:
        if <condition> {
            DO SOMETHING;
        }
        else {
            DO SOMETHING ELSE;
        }

Loops:

    There are 3 types of loops:

        1. While Loop:
            while <condition> {
                DO SOMETHING;
            }

        2. For-From-To-Skip Loop:
            for <loop_counter_name> from <start> to <end> (skip <skip>) {
                DO SOMETHING;
            }

            * Notice that the for loop starts counting from start to end including start and end.
            * The skip part is optional, with including it, the loop will skip <skip> numbers, example:
                for i from 1 to 10 skip 2 {
                    print i;
                }

                Output:
                    1
                    3
                    5
                    7
                    9

        3. For-In Loop:
            for <iterator_variable_name> in <data_structure> {
                DO SOMETHING;
            }

Functions:
    Syntax:
        function <function_name> (<arguments>, <optional_arg>=<default_value>) {
            FUNCTION BODY;
            return <value>;
        }

        * Every function must return a value, if you want to build a function that doesnt return value, return NO_VALUE;

    Another syntax for functions that take unknown number of arguments:
        function <function_name> takes from <from> to <to> as <name> (<arguments> {
            // All other arguments that arent in <arguments> are stored as array names <name>
            FUNCTION BODY;
            return <value>;
        }
"""