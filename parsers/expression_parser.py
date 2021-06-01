from parsers.lighting_command_node import LightingCommandNode
import re

number_pattern = '^(-?[0-9]+\\.?[0-9]*)$'
addition_pattern = '(\\s?\\+\\s?)'

# expression := number | operation
# operation := expression~operator~expression
# operator := multiplication | division | addition | subtraction


# https://gist.github.com/yelouafi/556e5159e869952335e01f6b473c4ec1

def parse_number(token):
    result = re.search(number_pattern, token)
    if result is None:
        return ParseFailure("a valid number", token)
    parse_result = ParseResult(token, result.group(1))
    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
    else:
        parse_result.value = int(parse_result.match)
    return parse_result


def parse_addition(token):
    result = re.search(addition_pattern, token)
    if result is None:
        return ParseFailure("expr + expr", token)
    parse_result = ParseResult(token, result.group(1))
    # TODO: need to resolve left and right.  So need a global expression parser
    # parse_result.value = parse_result.left.value + parse_result.right.value
    return parse_result


def parse_expression(token):
    result = parse_addition(token)
    if type(result) is ParseFailure:
        return parse_number(token)

    if result.left is not None:
        result.left = parse_expression(result.left)
    if result.right is not None:
        result.right = parse_expression(result.right)
    return result


class ParseResult:

    def __init__(self, token, match):
        self.token = token
        self.match = match
        self.left = None
        self.right = None
        self.value = None
        candidate_left = token[0:token.find(match)]
        candidate_right = token[token.find(match) + len(match):].strip()
        if len(candidate_right) > 0:
            self.right = candidate_right
        if len(candidate_left) > 0:
            self.left = candidate_left


class ParseFailure:
    
    def __init__(self, expected, actual):
        self.actual = actual
        self.expected = expected

