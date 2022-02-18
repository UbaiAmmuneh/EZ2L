# EZ2L

## Usage

1. Download the `EZ2L.py` file.
2. Create a file with the extension of `.ez2l`, example: `main.ez2l`.
3. Put your code inside of the file you just created.
4. From the command line run, `python PATH/TO/EZ2L.py PATH/TO/YOUR/CODE`, Example: `python EZ2L.py main.ez2l`.

## Introduction
**EZ2L** (short for _Easy To Learn_) is a simple "_programming language_" that is built by **Ubai Ammuneh**.

**EZ2L**'s syntax is very similar to _spoken English_ what makes it easy to learn and use. 

## Variables
There are 6 Variable Types in **EZ2L**:

#### Null
Null is a special variable type that represents an empty variable.

Null variables have only one value: `null`.

#### Boolean
Boolean variables are variables that hold the values `true / True` or `false / False`.

Boolean variables are mostly used in conditions.

#### Number
Number variables can hold any number: `0`, `3.14`, `-1.5`, ...

Note that for negative values the `-` sign must be close to the number.

For example: `- 1.5` is considered as a mathematical subtraction operation where the first operator is missing 
(which will cause an error) and the second operator is `1.5`.

#### String
Strings are any sequence of characters.
Strings must start and end with a `'` or `"`.

For example: `"Hello World!"`, `'Hello World!'` are both strings that contain the characters sequence `Hello World!`.

#### Array
Arrays are variables that store multiple values (Collections).
Arrays must start with `[` and end with `]`.

For example: `[1, 2, 3]` is an array that stores 3 values which are `1`, `2`, `3`.

#### Map
Maps are another type of collections that map **Keys** to **Values**.
Maps must start with `{` and end with `}`.

For example: `{john: 1, michael: 2}` is a map that maps the key `john` to the value `1` and the key `michael` to value `2`.

## Variables Declaration and Deletion
##### Declaring variables is done using the `set` keyword.

**Syntax**: `set <variable_name> to <value>`.

Variables naming rules:
+ Variable name can only contain,
  + Underscore: `_`
  + Letters: `a to z`, `A to Z`
  + Numbers: `0 to 9`
+ Variable name can't start with a number.  

**Examples**:

+ `set x to 1` Declares a new variable called `x` with the value `1`

+ `set arr to [1, 2, 3]` Declares a variable called `arr` with the value `[1, 2, 3]`

##### Variables can also be deleted using the `del` keyword.

**Syntax**: `del <var_name>`.

**Example**:

`del x` Deletes the variable `x`

##### Checking type of variable is done using the `typeof` keyword

**Syntax**: `typeof <variable>`

**Example**:

`print typeof 1` This command prints `number`.

\* `print` is a keyword explained below.

## Input / Output
#### Inputs are taken from user using the `input` keyword.

**Syntax**: `input`

A message can be printed before the input using:

**Syntax**: `input message <message>`

#### Outputs to the screen are done using the `print` keyword.

**Syntax**: `print <output>`.

Note that the `print` keyword prints the output on one line then goes to a new line.
You can change the postfix of the printed output (which is by default `\n`) using:

**Syntax**: `print <output> end with <postfix>`

**Example**:

    set x to input message 'Enter your name: '
    print 'Hi,' end with ' '
    print x end with ' !'
    
    Output:
    
    Enter your name: Ubai
    Hi, Ubai !

## Comments
There are 2 types of comments that can be used in **EZ2L**:
+ Single-Line Comment: which is a comment that starts somewhere in a line of code, and end on the end of the line.
**Syntax**: `// Comment ...`
+ Multi-Line Comment: which is a comment that its start and end are set, and can exceed the one line.
**Syntax**: `/* Comment */`.

**Example**:

    // This is a comment
    
    /* This is
       a multi-line
       comment */

## Collection Operations

| Command  |                    Syntax                    |                                           Usage                                    |                   Example                        |
| -------- | -------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------ |
| `get`    | `get <index> from <collection>`              | Used to get an element in specific index in collection                             | `get 0 from [1, 2, 3]` --> `1`                     |
| `in`     | `<element> in <collection>`                  | Used to check if element is in collection                                          | `3 in [1, 2, 3]` --> `true`                      |
| `add`    | `add <element> to <collection>`              | Used to add element to collection                                                  | `add [4] to [1, 2, 3]` --> `[1, 2, 3, 4]`        |
| `slice`  | `slice <collection> from <start> to <end>`   | Used to slice a collection to get all elements from index `<start>` to `<end> - 1` | `slice [1, 2, 3, 4, 5] from 1 to 3` --> `[2, 3]` |
| `length` | `length of <operator>`                       | Used to get how many items are in the collection                                   | `length of 'abcd'` --> `4`                       |

The `add` operations has a special syntax:
+ If the collection is a string, `add 'STRING' to <collection>` Example: `add 'd' to 'abc'` --> `'abcd'`
+ If the collection is an array, `add [ELEMENTS} to <collection>` Example: `add [4, 5] to [1, 2, 3]` --> `[1, 2, 3, 4, 5]`
+ If the collection is a map, `add <key>:<value> to <collection>` Example: `add c:3, d:4 to {a:1, b:2}` --> `{a:1, b:2, c:3, d:4}`

## Numeric Operations

There are 2 variables that are built-in:
+ `MATH.E` which is the natural basis, its value is: 2.718281828459045
+ `MATH.PI` which is the ratio of a circle's circumference to its diameter, its value is: 3.141592653589793

|            Operation             |                        Syntax                    |                 Example           |
| -------------------------------- | ------------------------------------------------ | --------------------------------- |
| `+` (Addition)                   | `<operator1> + <operator2>`                      | `1 + 2` --> `3`                   |
| `-` (Subtraction)                | `<operator1> - <operator2>`                      | `1 - 2` --> `-1`                  |
| `*` (Multiplication)             | `<operator1> * <operator2>`                      | `1 * 2` --> `2`                   |
| `/` (Division)                   | `<operator1> / <operator2>`                      | `1 / 2` --> `0.5`                 |
| `%` (Modulo)                     | `<operator1> % <operator2>`                      | `5 % 2` --> `1`                   |
| `raise` (Power Raise)            | `raise <operator> to power <power>`              | `raise 2 to power 3` --> `8`      |
| `sqrt` (Square Root)             | `sqrt of <operator>`                             | `sqrt of 4` --> `2.0`             |
| `abs` (Absolute Value)           | `abs of <operator>`                              | `abs of -2` --> `2`               |
| `floor` (Floor)                  | `floor of <operator>`                            | `floor of 2.9` --> `2`            |
| `ceil` (Ceiling)                 | `ceil of <operator>`                             | `ceil of 3.1` --> `4`             |
| `ln` (Natural Logarithm)         | `ln <operator>`                                  | `ln 1` --> `0`                    |
| `log` (Logarithm)                | `log <operator> base <base>`                     | `log 100 base 10` --> `2`         |
| `sin` (Sine)                     | `sin <degree>`   (`<degree>` must be in radians) | `sin 0` --> `0`                   |
| `cos` (Cosine)                   | `cos <degree>`   (`<degree>` must be in radians) | `cos MATH.PI` --> `-1`            |
| `tan` (Tangent)                  | `tan <degree>`   (`<degree>` must be in radians) | `tan MATH.PI / 4` --> `1`         |
| `asin` (Arc Sine)                | `asin <degree>`  (`<degree>` must be in radians) | `asin 0` --> `0`                  |
| `acos` (Arc Cosine)              | `acos <degree>`  (`<degree>` must be in radians) | `acos 1` --> `0`                  |
| `atan` (Arc Tangent)             | `atan <degree>`  (`<degree>` must be in radians) | `atan 0` --> `0`                  |
| `sinh` (Hyperbolic Sine)         | `sinh <degree>`  (`<degree>` must be in radians) | `sinh 0` --> `0`                  |
| `cosh` (Hyperbolic Cosine)       | `cosh <degree>`  (`<degree>` must be in radians) | `cosh 0` --> `1`                  |
| `tanh` (Hyperbolic Tangent)      | `tanh <degree>`  (`<degree>` must be in radians) | `tanh 0` --> `0`                  |
| `asinh` (Arc Hyperbolic Sine)    | `asinh <degree>` (`<degree>` must be in radians) | `asinh 0` --> `0`                 |
| `acosh` (Arc Hyperbolic Cosine)  | `acosh <degree>` (`<degree>` must be in radians) | `acosh 1` --> `0`                 |
| `atanh` (Arc Hyperbolic Tangent) | `atanh <degree>` (`<degree>` must be in radians) | `atanh 0` --> `0`                 |
| `factorial` (Factorial)          | `factorial of <operator>`                        | `factorial of 5` --> `120`        |
| `degrees` (Radians To Degrees)   | `degrees of <radians>`                           | `degrees of MATH.PI / 2` --> `90` |
| `radians` (Degrees To Radians)   | `radians of <degrees>`                           | `radians of 0` --> `0`            |

Note that the `-` operator requires at least one white space after it.

For Example, the command `1-1` is compiled as calling 2 numbers the first one is `1` and the second one is `-1`, which will yield to an error

## Bitwise Operations

|   Operation   |               Syntax             |           Example         |
| ------------- | -------------------------------- | ------------------------- |
| `shift left`  | `<operator> shift left <shift>`  | `5 shift left 2` --> `20` |
| `shift right` | `<operator> shift right <shift>` | `5 shift right 2` --> `1` |
| `bitand`      | `<operator1> bitand <operator2>` | `5 bitand 2` --> `0`      |
| `bitor`       | `<operator1> bitor <operator2>`  | `5 bitor 2` --> `7`       |
| `bitnot`      | `bitnot <operator>`              | `bitnot 2` --> `-3`       |

## Conditions

####Using conditions is done using the `if else` keywords
**Syntax**:
    
    if <condition>
        code
    end if

    - OR -

    if <condition>
        code
    else
        code 2
    end if

Conditions are Block Coded which means, and if block must end with `end if`.

#### Comparison Operations

Using conditions is mostly done by comparing 2 values.
There are 6 **Comparison Operations** in **EZ2L**:

|       Operation         |                    Syntax                       |                 Example                |
| ----------------------- | ----------------------------------------------- | -------------------------------------- |
| `equals`                | `<operator1> equals <operator2>`                | `2 equals 2` --> `true`                |
| `different from`        | `<operator1> different from <operator2>`        | `1 different from 2` --> `true`        |
| `greater than`          | `<operator1> greater than <operator2>`          | `1 greater than 2` --> `false`         |
| `smaller than`          | `<operator1> smaller than <operator2>`          | `1 smaller than 2` --> `true`          |
| `greater or equal than` | `<operator1> greater or equal than <operator2>` | `2 greater or equal than 2` --> `true` |
| `smaller or equal than` | `<operator1> smaller or equal than <operator2>` | `2 smaller or equal than 2` --> `true` |

#### Logical Operations

| Operation |            Syntax           |            Example           |
| --------- | --------------------------- | ---------------------------- |
| `or`      | `<operator> or <operator>`  | `true or false` --> `true`   |
| `xor`     | `<operator> xor <operator>` | `true xor false` --> `true`  |
| `and`     | `<operator> and <operator>` | `true and false` --> `false` |
| `not`     | `not <operator>`            | `not false` --> `true`       |

## Loops
There are 3 types of loops in `EZ2L`:

#### For-From-To Loop

**Syntax**:

    for <counter> from <start> to <end>
        code
    end for
    
    - OR -
    
    for <counter> from <start> to <end> jump <steps>
        code
    end for

For-From-To loops on all numbers starting at `<start>` up to `<end>` **including `<start>` and not including `<end>`**.

`<counter>` is the loop counter, and it can be used as a variable inside the loop, note that after the loop is finished the `<counter>` variable will no longer be available.

**Example**:

    for i from 1 to 10 jump 2
        if i smaller than 9
            print i end with ', '
        else
            print i
        end if
    end for
    
    Output:
    
     1, 3, 5, 7, 9
     
 #### For-In Loop
 
**Syntax**:

    for <element> in <collection>
        code
    end for

For-In loops are used to loop on a specific collection (array / map).

**Example**:

    for i in [1, 2, 3, 4, 5]
        if i smaller than 5
            print i end with ', '
        else
            print i
        end if
    end for
    
    Output:
    
    1, 2, 3, 4, 5
    
#### While Loop

**Syntax**:

    while <condition>
        code
    end while
    
While Loops are used to run code while a condition is `true`, once it turns `false` the while loop finishes.

**Example**:

    set x to 1
    
    while x smaller than 10
        if x smaller than 9
            print i end with ', '
        else
            print i
        end if
        
        set x to x + 1
    end while
    
    Output:
    
    1, 2, 3, 4, 5, 6, 7, 8, 9
     
     

## Functions

#### Function Declaration is done using the `function` keyword

**Syntax**:

    function <function_name> (<args>)
        function body
    end function
    
    Calling the function:
    <function_name>(<args>)

Function naming rules are the same as variable naming rules.

There are 2 types of arguments, required arguments and default arguments:
+ Required Arguments: Arguments that require a value to be passed to the function.
+ Default Arguments: Arguments that have default values, and if no value was provided the default one will be used. **Syntax**: `<arg_name>=<default_value>`

The `return` command is used in functions to return values, each function returns value, if function body doesn't return any values, `null` will automatically be returned.
    
**Example**:

    function sum(x, y=1)
        return x + y
    end function
    
    set x to sum(1)
    set y to print(3, 3)
    
    print x
    print y
    
    Output:
    
    2
    6
    

## Classes
#### Class Declaration is done using the `class` keyword

Classes are type of objects that have variables / properties and some functions.

**Syntax**:

    class <class_name>
        
        variables
            <class_variables>
        end variables
        
        constructor(<args>)
            <constructor_body>
        end constructor
        
        <functions>
    end class
    
Class Naming rules are the same as variable naming rules.

A class have 3 parts:
+ Variables Block: which includes all the class properties / variables separated by new line
+ Constructor Block: constructor is a special function that gets called when a new object from that class is declared.
+ Functions: all the functions of the class.

Note that calling a class variable/function inside of the class is done using: `<class_name>.<variable/function>`.

Calling a class variable/function outside the class: `<instance_name>.<variable/function>`.

Declaring a class object is done using the `create` keyword.

**Syntax**: `create <instance_name> from <class_name> initialize with <args>`

**Example**: 

    class Person
        
        variables
            name
            id
            gender
        end variables
        
        constructor(_name, _id, _gender)
            set Person.name to _name
            set Person.id to _id
            set Person.gender to _gender
        end constructor
        
        function get_info()
            return {'name': Person.name, 'id': Person.id, 'gender': Person.gender}
        end function
    end class
    
    create john from Person initialize with 'John', 123, 'Male'
    set john.id to 333
    
    print john.id
    print john.get_info()
    
    Output:
    333
    {'name': 'John', 'id': 333, 'gender': 'Male'}
    
            

## Other Operations

#### Random Operations

|   Operation   |                        Syntax                        |                    Example                   |
| ------------- | ---------------------------------------------------- | -------------------------------------------- |
| `pick from`   | `pick from <array>`                                  | `pick from [1, 2, 3]` --> `1`                |
| `pick number` | `pick number start <start> stop <end> (jump <step>`) | `pick number start 1 stop 10 jump 3` --> `4` |
| `shuffle`     | `shuffle <array>`                                    | 

**Example** on `shuffle`:

    set x to [1, 2, 3]
    shuffle x
    print x
    
    Output:
    [2, 1, 3]

#### Time Operations

| Operation |        Syntax     |                               Usage                         |                        Example                  |
| --------- | ----------------- | ----------------------------------------------------------- | ----------------------------------------------- |
| `sleep`   | `sleep <seconds>` | Used to pause the program for couple seconds                | `sleep 5`                                       |
| `time`    | `time`            | Used to get how many seconds passed from Jan. 1 1970        | `time` --> `1111111111`                         |
| `ctime`   | `ctime <seconds>` | Used to print date based on seconds passed from Jan. 1 1970 | `ctime 111111111` -> `Fri Mar 18 03:58:31 2005` |

#### Files Operations

|   Operation   |                 Syntax             |                                                 Example                                       |
| ------------- | ---------------------------------- | --------------------------------------------------------------------------------------------- |
| `dir`         | `dir <path> (only files/dirs)`     | `dir 'C:\\' only files` --> All the files at 'C' disk                                         |
| `create file` | `create file <filename> at <path>` | `create file 'a.txt' at 'C:\\'`                                                               |
| `delete file` | `delete file <filepath>`           | `delete file 'C:\\a.txt'`                                                                     |
| `read`        | `read from <filepath>`             | `read from 'C:\\a.txt'` --> a list of all lines in file 'C:\a.txt'                            |
| `write`       | `write <line> to <filepath>`       | `write 'Hello World!' to 'C:\\a.txt'` --> writes a new line `Hello World!` in file 'C:\a.txt' |

#### The `import` operations
`import` is used to import a file into another.

**Syntax**: `import <filename>`

**Example**:

    // File1.ez2l
    
    function sum(x, y)
        return x + y
    end function

#####

    // File2.ez2l
    
    import File1 // OR import File1.ez2l
    print sum(2, 3)
    
    Output:
    5

#### The `try` operations
`try` is used to catch errors in program.

**Syntax**: 

    try
        <CODE>
    catch
        <CODE>
    end try

**Example**:

    try
        print 1 / 0
    catch
        print 'Cant divide 1 by 0'
    end try

    Output:
    Cant divide 1 by 0
    
