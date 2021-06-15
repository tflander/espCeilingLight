import re

from parsers.result_objects import *


def parse_generic(token, pattern, value_type, value_resolver=None):
    result = re.search(pattern, token)
    if result is None:
        return ParseFailure(token, token)
    parse_result = ParseResult(token, result.group(1), value_type)
    if value_resolver is not None:
        parse_result.value = value_resolver(parse_result.match)

    return parse_result
