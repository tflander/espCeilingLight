import re
from parsers.expression_parser import CombineResult
from parsers.parser_constants import ExpressionValueTypes

function_pattern = "^([_a-zA-Z][_0-9a-zA-Z]*)\\((.*)\\)"


def parse_function(original_token):
    result = re.match(function_pattern, 'random(0,1023)')
    match = [result.group(1), result.group(2)]
    return CombineResult(original_token, match, ExpressionValueTypes.FUNCTION)
