class LightingCommandNodeTypes:
    EXPR = 1


class ExpressionValueTypes:
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
    ASSIGNMENT = "="
    COMMENT = "//"
