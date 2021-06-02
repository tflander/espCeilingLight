import re

from parsers.parser_constants import ExpressionValueTypes

number_pattern = '^(-?[0-9]+\\.?[0-9]*)'
hex_number_pattern = '^(0x[0-9,a-f,A-F]+)'
addition_pattern = '^(\\s?\\+\\s?)'
multiplication_pattern = '^(\\s?\\*\\s?)'
division_pattern = '^(\\s?\\/\\s?)'
subtraction_pattern = '^(\\s?\\-\\s?)'


# expression := number | operation
# operation := expression~operator~expression
# operator := multiplication | addition | division | subtraction
# number := int | float | hex


def parse_number(token):
    result = parse_hex(token)
    if type(result) == ParseFailure:
        result = parse_int_or_float(token)
    return result


def parse_int_or_float(token):
    result = re.search(number_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), None)

    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.FLOAT
    else:
        parse_result.value = int(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.INT
    return parse_result


def parse_hex(token):
    result = re.search(hex_number_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), None)

    parse_result.value = int(parse_result.match, 16)
    parse_result.result_type = ExpressionValueTypes.HEX

    return parse_result


def parse_addition(token):
    return parse_operation(token, addition_pattern, ExpressionValueTypes.ADDITION)


def parse_multiplication(token):
    return parse_operation(token, multiplication_pattern, ExpressionValueTypes.MULTIPLICATION)


def parse_division(token):
    return parse_operation(token, division_pattern, ExpressionValueTypes.DIVISION)


def parse_subtraction(token):
    return parse_operation(token, subtraction_pattern, ExpressionValueTypes.SUBTRACTION)


def parse_operation(token, pattern, value_type):
    result = re.search(pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), value_type)

    return parse_result


expression_parsers = [parse_number, parse_addition, parse_multiplication, parse_division, parse_subtraction]


def parse_expression(original_token):
    token_results = []
    token = original_token
    while len(token) > 0:
        latest_result = None
        for parser in expression_parsers:
            result = parser(token)
            if type(result) == ParseResult:
                latest_result = result
                token = result.rest
                break
        if latest_result is None:
            return ParseFailure(token, original_token, 1)
        token_results.append(result)

    combined_results = combine_expression_results(token_results)
    if len(combined_results) != 1:
        return ParseFailure("TODO: Some decent handling", original_token, 1)
    return combined_results[0]


def combine_multiplication_results(results):
    return combine_operator_results(results, ExpressionValueTypes.MULTIPLICATION, lambda a, b: a*b)


def combine_addition_results(results):
    return combine_operator_results(results, ExpressionValueTypes.ADDITION, lambda a, b: a+b)


def combine_division_results(results):
    return combine_operator_results(results, ExpressionValueTypes.DIVISION, lambda a, b: a/b)


def combine_subtraction_results(results):
    return combine_operator_results(results, ExpressionValueTypes.SUBTRACTION, lambda a, b: a-b)


expression_combinators = [
    combine_multiplication_results,
    combine_division_results,
    combine_addition_results,
    combine_subtraction_results
]


def combine_expression_results(results):
    combined_results = results
    for combinator in expression_combinators:
        while True:
            combined_results, combined = combinator(combined_results)
            if not combined:
                break
    return combined_results


def combine_operator_results(results, operator_value_type, value_combiner):
    for i, result in enumerate(results):
        if result.result_type == operator_value_type:
            token = results[i-1].match + results[i].match + results[i+1].match
            combined_result = ParseResult(token, token, ExpressionValueTypes.OPERATION)
            combined_result.value = value_combiner(results[i - 1].value, results[i + 1].value)
            return results[:i-1] + [combined_result] + results[i+2:], True
    return results, False


class ParseResult:

    def __init__(self, token, match, result_type):
        self.result_type = result_type
        self.token = token
        self.match = match
        self.value = None
        if match is not None:  # TODO: true when combining.  Should we have a combine result type?
            self.rest = token[len(match):]


class ParseFailure:
    
    def __init__(self, errored_token, text, line):
        self.line = line
        pos = text.index(errored_token) + 1
        if pos > 1:
            self.message = [
                "Syntax Error, line " + str(line),
                "  " + text,
                "  " + (" " * pos) + "^"
        ]

