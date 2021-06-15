from parsers.operator_parser import *
from parsers.parser_core import *
from parsers.result_objects import *

function_pattern = "^([_a-zA-Z][_0-9a-zA-Z]*)\\((.*)\\)"
comma_pattern = "^(\\,)"

# expression := number | variable_identifier | operation | expression in parens
#               | function # TODO: list lookup, dictionary lookup
# operation := expression~operator~expression
# operator := exponent | multiplication | addition | division | subtraction  # TODO:  mod
# number := int | float | hex


def parse_function(original_token):
    result = re.match(function_pattern, original_token)
    if result is None:
        return ParseFailure(original_token, original_token)
    function_name = result.group(1)
    function_parameters = parse_function_parameters(result.group(2))
    if type(function_parameters) is ParseFailure:
        return ParseFailure(function_parameters.errored_token, original_token)
    match = original_token[result.pos:result.endpos]
    result = ParseResult(original_token, match, ExpressionValueTypes.FUNCTION)
    result.function_name = function_name
    result.function_parameters = function_parameters
    return result


expression_parsers = [parse_number, parse_operation, parse_function, parse_variable_identifier, parse_left_paren, parse_right_paren]


def get_expression_token(original_token, token):
    return get_token(original_token, token, expression_parsers)


def tokenize_expression(original_token):
    token_results = []
    token = original_token
    while len(token) > 0:
        latest_result = get_expression_token(original_token, token)
        if type(latest_result) is ParseFailure:
            return latest_result
        token = latest_result.rest
        token_results.append(latest_result)

    return token_results


def combine_expression_tokens(original_token, token_results):

    combined_results = combine_expression_results(token_results)
    if type(combined_results) == CombineFailure:
        failure = ParseFailure("", original_token)

        failure.message = [
            "Syntax Error",
            "  " + original_token,
            "  " + (" " * len(combined_results.errored_token)) + "^"
        ]

        failure.inner = combined_results
        return failure

    if len(combined_results) != 1:
        failure = CombineFailure(original_token, 1)
        failure.message = ["unexpected combine error for token " + original_token]
        return failure
    return combined_results[0]


def parse_expression(original_token):

    token_results = tokenize_expression(original_token)
    if type(token_results) == ParseFailure:
        return token_results

    return combine_expression_tokens(original_token, token_results)


def combine_parens(results):
    left_paren_pos = None
    for i, result in enumerate(results):
        if result.result_type == ExpressionValueTypes.LEFT_PAREN:
            left_paren_pos = i
        if result.result_type == ExpressionValueTypes.RIGHT_PAREN:

            if left_paren_pos is None:
                failure = CombineFailure(results[0].token)
                failure.message = "unmatched right paren: " + results[0].token
                return failure, False

            inner_expression = results[left_paren_pos+1: i]
            inner_result = combine_expression_results(inner_expression)
            return results[:left_paren_pos] + inner_result + results[i+1:], True

    if left_paren_pos is not None:
        failure = CombineFailure(results[0].token)
        failure.message = "unmatched left paren: " + results[0].token
        return failure, False

    return results, False


# TODO: use operator combinator
expression_combinators = [
    combine_parens,
    combine_exponent_results,
    combine_multiplication_results,
    combine_division_results,
    combine_addition_results,
    combine_subtraction_results
]


def combine_expression_results(results):
    return combine_results(results, expression_combinators)


def consume_comma(token):
    return parse_generic(token, comma_pattern, ExpressionValueTypes.COMMA)


# TODO: call this parse_expression list?
def parse_function_parameters(original_token):
    results = []
    token = original_token
    while len(token) > 0:
        result = get_expression_token(original_token, token)
        if type(result) is ParseFailure:
            result = consume_comma(token)

        if type(result) == ParseFailure:
            return result
        results.append(result)
        token = result.rest.strip()

    return results

