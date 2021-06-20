import re

from parsers.parser_constants import ExpressionValueTypes
from parsers.parser_core import parse_generic
from parsers.result_objects import ParseResult

time_parameter_pattern = "([0-9]+)(s|m|ms)"
time_pattern = "^" + time_parameter_pattern + "$"


def parse_classic_time(token):
    compiled_time_pattern = re.compile(time_pattern)
    # TODO: precompile all regex patterns?
    result = parse_generic(token, compiled_time_pattern, ExpressionValueTypes.TIME)
    if type(result) is ParseResult:
        delay_time = float(result.match)
        delay_unit = result.rest
        if delay_unit == 's':
            delay_time *= 1000
        elif delay_unit == 'm':
            delay_time *= 60000
        result.value = delay_time
    return result
