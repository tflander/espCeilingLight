import re
from parsers.expression_parser import CombineResult, ParseFailure
from parsers.parser_constants import ExpressionValueTypes

function_pattern = "^([_a-zA-Z][_0-9a-zA-Z]*)\\((.*)\\)"


def parse_function(original_token):
    result = re.match(function_pattern, original_token)
    if result is None:
        return ParseFailure(original_token, original_token)
    match = [result.group(1), result.group(2)]
    return CombineResult(original_token, match, ExpressionValueTypes.FUNCTION)
