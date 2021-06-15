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


def is_valid_operand(result):
    return result.value is not None \
        or result.result_type == ExpressionValueTypes.VARIABLE \
        or result.result_type == ExpressionValueTypes.OPERATION


def combine_operator_results(results, operator_value_type, value_combiner):
    for i, result in enumerate(results):
        if result.result_type == operator_value_type:
            left_operand = results[i-1]
            right_operand = results[i+1]
            token = left_operand.match + results[i].match + right_operand.match
            combined_result = ParseResult(token, operator_value_type, ExpressionValueTypes.OPERATION)

            if not is_valid_operand(left_operand) or not is_valid_operand(right_operand):
                failure = CombineFailure(token)
                if not is_valid_operand(left_operand):
                    failure.message = "invalid left operand: " + left_operand.match
                else:
                    failure.message = "invalid right operand: " + right_operand.match
                return failure, False

            if left_operand.value is not None and right_operand.value is not None:
                combined_result.value = value_combiner(left_operand.value, right_operand.value)
            else:
                combined_result.left = left_operand
                combined_result.right = right_operand
            return results[:i-1] + [combined_result] + results[i+2:], True
    return results, False

