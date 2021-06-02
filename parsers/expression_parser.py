from parsers.lighting_command_node import LightingCommandNode
import re

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
    parse_result = ParseResult(token, result.group(1))

    # TODO: replace this crap with a parser sequence
    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
    else:
        parse_result.value = int(parse_result.match)
    return parse_result


def parse_addition(token):
    result = re.search(addition_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1))

    return parse_result


def parse_multiplication(token):
    result = re.search(multiplication_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1))

    return parse_result


basic_parsers = [parse_number, parse_addition, parse_multiplication]


def parse_expression(original_token):
    results = []
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
        results.append(result)

    # TODO: for now return results.  Need to apply combinator function
    return results


class ParseResult:

    def __init__(self, token, match):
        self.token = token
        self.match = match
        self.value = None
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

