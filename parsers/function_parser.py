import re
from parsers.expression_parser import *
from parsers.parser_constants import ExpressionValueTypes

function_pattern = "^([_a-zA-Z][_0-9a-zA-Z]*)\\((.*)\\)"
comma_pattern = "^(\\,)"

def parse_function(original_token):
    result = re.match(function_pattern, original_token)
    if result is None:
        return ParseFailure(original_token, original_token)
    match = [result.group(1), result.group(2)]
    return CombineResult(original_token, match, ExpressionValueTypes.FUNCTION)


def consume_comma(token):
    return parse_generic(token, comma_pattern, ",")  # TODO: figure out where the comma value type belongs


# TODO: call this parse_expression list?
def parse_function_parameters(original_token):
    results = []
    token = original_token
    while len(token) > 0:
        result = get_expression_token(original_token, token)
        if type(result) is ParseFailure:
            result = consume_comma(token)

        # TODO: need test where result failure is here
        results.append(result)
        token = result.rest

        # TODO: combine results
    return results
