import re

from parsers.parser_constants import ExpressionValueTypes
from parsers.result_objects import *

number_pattern = '^(-?[0-9]+\\.?[0-9]*)'
hex_number_pattern = '^(0x[0-9a-fA-F]+)'
variable_identifier_pattern = '^([_a-zA-Z][_0-9a-zA-Z]*)'


def parse_variable_identifier(token):
    return parse_generic(token, variable_identifier_pattern, ExpressionValueTypes.VARIABLE)


def parse_number(token):
    result = parse_hex(token)
    if type(result) == ParseFailure:
        result = parse_int_or_float(token)
    return result


def parse_int_or_float(token):
    result = re.search(number_pattern, token)
    if result is None:
        return ParseFailure(token, token)
    parse_result = ParseResult(token, result.group(1), None)

    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.FLOAT
    else:
        parse_result.value = int(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.INT
    return parse_result


def parse_hex(token):
    return parse_generic(token, hex_number_pattern, ExpressionValueTypes.HEX, lambda v: int(v, 16))


def parse_generic(token, pattern, value_type, value_resolver=None):
    result = re.search(pattern, token)
    if result is None:
        return ParseFailure(token, token)
    parse_result = ParseResult(token, result.group(1), value_type)
    if value_resolver is not None:
        parse_result.value = value_resolver(parse_result.match)

    return parse_result


def get_token(original_token, token, parsers):
    latest_result = None
    for parser in parsers:
        result = parser(token)
        if type(result) == ParseResult:
            latest_result = result
            break
    if latest_result is None:
        return ParseFailure(token, original_token)
    return result


def combine_results(results, combinators):
    combined_results = results
    for combinator in combinators:
        while True:
            combined_results, combined = combinator(combined_results)
            if type(combined_results) == CombineFailure:
                return combined_results
            if not combined:
                break
    return combined_results
