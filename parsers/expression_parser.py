import re

from parsers.parser_constants import ExpressionValueTypes

number_pattern = '^(-?[0-9]+\\.?[0-9]*)'

addition_pattern = '^(\\s?\\+\\s?)'
multiplication_pattern = '^(\\s?\\*\\s?)'

# expression := number | operation
# operation := expression~operator~expression
# operator := multiplication | addition  TODO: division and subtraction
# number := int | float TODO: hex


# https://gist.github.com/yelouafi/556e5159e869952335e01f6b473c4ec1


def parse_number(token):
    result = re.search(number_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), None)

    # TODO: replace this crap with a parser sequence
    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.FLOAT
    else:
        parse_result.value = int(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.INT
    return parse_result


def parse_addition(token):
    result = re.search(addition_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), ExpressionValueTypes.ADDITION)

    return parse_result


def parse_multiplication(token):
    result = re.search(multiplication_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), ExpressionValueTypes.MULTIPLICATION)

    return parse_result


basic_parsers = [parse_number, parse_addition, parse_multiplication]


def parse_expression(original_token):
    token_results = []
    token = original_token
    while len(token) > 0:
        latest_result = None
        for parser in basic_parsers:
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


def combine_expression_results(results):
    combined_results = results
    while True:
        combined_results, combined = combine_multiplication_results(combined_results)
        if not combined:
            break

    while True:
        combined_results, combined = combine_addition_results(combined_results)
        if not combined:
            break
    return combined_results


def combine_multiplication_results(results):
    return combine_operator_results(results, ExpressionValueTypes.MULTIPLICATION, lambda a, b: a*b)


def combine_addition_results(results):
    return combine_operator_results(results, ExpressionValueTypes.ADDITION, lambda a, b: a+b)


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
        if match is not None:  # TODO: true when combinining.  Should we have a combine result type?
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

