import re

from parsers.parser_constants import ExpressionValueTypes
from parsers.parser_core import parse_generic
from parsers.result_objects import ParseResult

time_pattern = "^([0-9]+)(s|m|ms)$"


class TimeParser:

    compiled_time_pattern = re.compile(time_pattern)

    @staticmethod
    def parse(token):
        result = parse_generic(token, TimeParser.compiled_time_pattern, ExpressionValueTypes.TIME)
        if type(result) is ParseResult:
            delay_time = float(result.match)
            delay_unit = result.rest
            if delay_unit == 's':
                delay_time *= 1000
            elif delay_unit == 'm':
                delay_time *= 60000
            result.value = delay_time
        return result
