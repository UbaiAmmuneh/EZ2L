# EZData Interpreter

EZData is a Programming Language I created to learn more about Programming Languages and Data Structures.

EZData has a syntax close to spoken English to help new programmers write code easier.

# Syntax
EZData has an easy understandable syntax.<br>
+ Each line in program must end with `;`. There are couple operations that don't end with a semi-colon:
  + If / Else Statements
  + Loops
  + Functions Declaration
  + Classes Declaration
+ There are 2 types of comments:
  + Inline Comments: this kind of comments are placed at the end of a line of code, and must be preceded by `//`
  + Multi-Line Comments: comments that need to be on multiple lines must be written between `/*` and `*/`<br><br>
    +     print('Hello World!');  // I am an inline comment
          /* I am a 
             Multi-Line
             Comment
          */ 
+ Nesting operation inside another one or a data structure inside other needs to be included inside pair of parenthesis:

  +      if(length of (join 'a' with 'b')) {  // Note the '(' before the join keyword

# I/O
EZData has basic I/O implementation, it has 2 main functions for the I/O process.<br>
+ ##### Outputting to screen:
  Outputs are displayed using the `print` keyword. Example:
  <pre>
    print('Hello World!');
    
    Output:
    
    'Hello World!'
  </pre>
  The `print` can take an argument to determine the end of the printed text, default is newline (`\n`).
  <pre>
    print('Line 1', end with ' ');
    print('Line 2', end with '\nNew Line\n');
    print('Line 3');
    
    Output:
    Line 1 Line 2
    New Line
    Line 3
  </pre>
  In order to print a variable connected to a string use the special symbol `${variable_name}` in string.
  <pre>
    x = 1;
    print('x is ${x}!');
    
    Output:
    
    'x is 1!'
    ''
  </pre>
  ##### String Escaping:
  Strings can include special characters that have different rules on display from other strings.<br>
  Here is a list of most common String Escape Sequences:
  
  <pre>
        Escape Sequence  |      Meaning
       __________________|_______________________________________
             \\          |   Back Slash(\)
             \'          |   Single Quote(')
             \"          |   Double Quote(")
             \a          |   ASCII Bell (BEL)
             \b          |   ASCII Backspace (BS)
             \f          |   ASCII Formfeed (FF)
             \n          |   ASCII Linefeed (LF)
             \r          |   ASCII Carriage Return (CR)
             \t          |   ASCII Horizontal Tab (TAB)
             \v          |   ASCII Vertical Tab (VT)
             \ooo        |   ASCII character with octal value ooo
             \xhh...     |   ASCII character with hex value hh...
             \$          |   Dollar Sign
  </pre>
     
+ ##### Taking inputs from user:
  Inputs from user are taken using the `input` keyword. Example:
  <pre>
    print('Enter a number:', end with ' ');
    number = input;
    print('You entered ${number}');
    
    Output:
    
    Enter a number: 5
    You entered 5
  </pre>

+ ##### Working with files
      ... Coming Soon ...

# Variables

###
Variables are a very important part of code writing. Declaration of variables is done using the `=` symbol:<br>
`<variable_name> = <variable_value>;`

Since EZData is a dynamic language, variables can change their type according to their value.

Variables can be also deleted for space efficiency by using the `del` keyword. 

Example:

    x = 1;
    print(typeof x); // Number
    
    x = 'Hi';
    print(typeof x); // String
    
    del x;
    print(x); // Error.VariableNotFound

The `typeof` keyword is used to get variable's type in the syntax shown above in the example.

<hr>

EZData supports Primitive and Non-Primitive Data Structures:

### Primitive Data Structures:
These are the most primitive or the basic data structures. They are the building blocks for data manipulation and contain pure, simple values of a data.

EZData has four primitive variable types:
+ Null
+ Boolean
+ Number
+ String

#### Null:
Null is a special data type, that indicates an empty variable:<br>

    x = null;
    print(x); // Nothing shows as output
    print(typeof x); // Null
    print(length of null); // -1
    print(x == null); // true
    
    if(x) {
        Unreachable Code;
    }

#### Boolean:
This built-in data type that can take up the values: `true` and `false`, which often makes them interchangeable with the numbers 1 and 0. 
<br>Booleans are useful in conditional and comparison expressions, just like in the following examples:


    x = 4;
    y = 2;
    
    print(x == y);
    
Outputs:<br>
`false`
    
    z = (x > y);
    
    print(z);
    
    if(z) {
        print('x is greater than y');
    } else {
        print('x is not greater than y');
    }

Outputs:<br> 
`true`<br>
`x is greater than y`

There are 4 supported operations between Booleans:
+ `and`: `x and y` is `true` if and only if `x` is `true` and `y` is `true`.
+ `or`: `x or y` is `true` if and only if `x` is `true` or `y` is `true` (or both are `true`).
+ `xor`: `x xor y` is `true` if and only if `x`, `y` have different values.
+ `not`: `not x` is `true` if and only if `x` is `false`.

#### Number:
You can use a number represent numeric data, including whole numbers and floating point numbers (numbers which end with a decimal figure) from negative infinity to infinity, like 4, -1, 3.14.

There are 6 operations that are supported between numbers:
+ `+`: a plus symbol is used to add 2 numbers together. Example: `print(5 + 2); // 7`
+ `-`: a minus symbol is used to subtract 2 numbers from each other. Example: `print(5 - 2); // 3`
+ `*`: a star / multiplication symbol is used to multiple 2 numbers. Example: `print(5 * 2); // 10`
+ `/`: a slash symbol is used to divide 2 numbers, it returns the whole number from the answer. Example: `print(5 / 2); // 2`
+ `%`: a modulo symbol is used to get the remainder from the division of 2 numbers. Example: `print(5 % 2); // 1`
+ `**`: double stars symbol is used to raise a number to power. Example: `print(5 ** 2); // 25`

#### String:
Strings are collections of alphabets, words or other characters.

EZData has built-in methods to manipulate strings:

Define Strings: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`x = 'Hello';`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`y = 'World';`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`z = 'Start Middle End';`<br>

Get Character: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(get x at 1);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'e'`

Repeat String: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(join (repeat 'Hip ' 2 times) with 'Hooray!');` &nbsp; Outputs: &nbsp; `'Hip Hip Hooray!'`<br>

Join Strings: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(join x with ' ' with y with '!');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'Hello World!'`<br>

Replace Substring: &nbsp;`print(replace 'hi' with 'hello' in 'hi world!');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'hello world!'`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(replace all 'a' with 'b' in 'abca');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'bbcb'`<br>

Capitalize String: &nbsp;&nbsp;&nbsp; `print(capitalize 'hello world!');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'Hello World!'`<br>

Uppercase String: &nbsp; `print(upper 'hello world!');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'HELLO WORLD!'`<br>

Lowercase String: &nbsp; `print(lower 'HELLO WORLD!');'` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'hello world!'`<br>

Length Of String: &nbsp;&nbsp; `print(length of 'Hello World!');` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `12`<br>

Index Of Substring: `print(index of 'World' in 'Hello World!');'` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `6`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(index of 'not found' in 'Hello World!');'` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `null`<br>

Slicing String: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(slice z end 5);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `Start`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(slice z start 13);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `End`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(slice z start 6 end 12);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `Middle`<br>

### Non-Primitive Data Structures:

Non-primitive types are the sophisticated members of the data structure family. They don't just store a value, but rather a collection of values in various formats.

EZData has 6 non-primitive variable types:
+ Array
+ Map
+ Linked List
+ Binary Search Tree
+ Stack
+ Graph

#### Array:
Array is the simplest and most used collection data structure.

EZData has built-in methods to manipulate arrays:

Define Array: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `arr = [3.14, -1, 'Hello World!', [1, 2, 3]];`

Get Element: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(get arr at 2);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `'Hello World!'`

Insert Element: &nbsp;&nbsp;&nbsp;&nbsp; `insert 42 to arr;` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(arr);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[3.14, -1, 'Hello World!', [1, 2, 3], 42]`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `insert 0 to arr at 0;` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(arr);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[0, 3.14, -1, 'Hello World!', [1, 2, 3], 42]`

Repeat Array: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(repeat [1, 2] 2 times);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[1, 2, 1, 2]`

Join Arrays: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(join [1, 2] with [3]);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[1, 2, 3]`

Replace Element:&nbsp; `print(replace 1 with 'a' in [1, 2, 3, 1]);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `['a', 2, 3, 1]`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(replace all 1 with 'a' in [1, 2, 3, 1]);` &nbsp; Outputs: &nbsp; `['a', 2, 3, 'a']`

Length Of Array: &nbsp;&nbsp; `print(length of [1, 2]);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `2`

Index Of Element:&nbsp; `print(index of 5 in [1, 3, 5]);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `2`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(index of 7 in [1, 3, 5]);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `null`

Slicing Array: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `print(slice [1, 2, 3, 4, 5] start 3);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[4, 5]`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(slice [1, 2, 3, 4, 5] end 3);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[1, 2, 3]`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(slice [1, 2, 3, 4, 5] start 2 end 4);` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outputs: &nbsp; `[3, 4]`

#### Map:
    ... Coming Soon ...

#### Linked List:
    ... Coming Soon ...
    Delete, Search

#### Binary Search Tree:
    ... Coming Soon ...

#### Red Black Tree:
    ... Coming Soon ...
    
#### AVL Tree:
    ... Coming Soon ...
    
#### WAVL Tree:
    ... Coming Soon ...

#### Stack:
    ... Coming Soon ...
    push, pop, top, isEmpty

#### Graph:
    ... Coming Soon ...

# Conditions and Loops:
    ... Coming Soon ...

# Functions
    ... Coming Soon ...

# Classes and Inheritance
    ... Coming Soon ...

# Other Built-In Features
    ... Coming Soon ...