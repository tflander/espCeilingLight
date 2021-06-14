import re
from parsers.expression_parser import *
from parsers.parser_constants import ExpressionValueTypes

function_pattern = "^([_a-zA-Z][_0-9a-zA-Z]*)\\((.*)\\)"
comma_pattern = "^(\\,)"


def parse_function(original_token):
    result = re.match(function_pattern, original_token)
    if result is None:
        return ParseFailure(original_token, original_token)
    function_parameters = parse_function_parameters(result.group(2))
    if type(function_parameters) is ParseFailure:
        return ParseFailure(function_parameters.errored_token, original_token)
    match = [result.group(1), function_parameters]
    return CombineResult(original_token, match, ExpressionValueTypes.FUNCTION)


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
        token = result.rest

    return results
