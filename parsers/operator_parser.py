from parsers.parser_core import *

left_paren_pattern = '^(\\s*\\(\\s*)'
right_paren_pattern = '^(\\s*\\)\\s*)'
addition_pattern = '^(\\s*\\+\\s*)'
multiplication_pattern = '^(\\s*\\*\\s*)'
division_pattern = '^(\\s*\\/\\s*)'
subtraction_pattern = '^(\\s*\\-\\s*)'
exponent_pattern = '^(\\s*\\^\\s*)'


def parse_addition(token):
    return parse_generic(token, addition_pattern, ExpressionValueTypes.ADDITION)


def parse_multiplication(token):
    return parse_generic(token, multiplication_pattern, ExpressionValueTypes.MULTIPLICATION)


def parse_division(token):
    return parse_generic(token, division_pattern, ExpressionValueTypes.DIVISION)


def parse_subtraction(token):
    return parse_generic(token, subtraction_pattern, ExpressionValueTypes.SUBTRACTION)


def parse_exponent(token):
    return parse_generic(token, exponent_pattern, ExpressionValueTypes.EXPONENT)


operation_parsers = [parse_addition, parse_multiplication, parse_division, parse_subtraction, parse_exponent]


def parse_operation(token):
    for parser in operation_parsers:
        result = parser(token)
        if type(result) is ParseResult:
            return result
    return result


def parse_left_paren(token):
    return parse_generic(token, left_paren_pattern, ExpressionValueTypes.LEFT_PAREN)


def parse_right_paren(token):
    return parse_generic(token, right_paren_pattern, ExpressionValueTypes.RIGHT_PAREN)
