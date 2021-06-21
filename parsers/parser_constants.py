class LightingCommandNodeTypes:
    EXPR = 1


class ExpressionValueTypes:
    TIME = 'time'
    EXPONENT = '^'
    COMMA = ","
    FUNCTION = "fn"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    INT = "int"
    FLOAT = "float"
    HEX = "hex"
    ADDITION = "+"
    MULTIPLICATION = "*"
    DIVISION = "/"
    SUBTRACTION = "-"
    OPERATION = "op"
    VARIABLE = "var"


class CommandTypes:
    END_LOOP = "end_loop"
    SLEEP = "sleep"
    COLOR = "color"
    FOR = "for"
    WHILE = "while"
    ASSIGNMENT = "="
    COMMENT = "//"
