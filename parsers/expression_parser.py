from parsers.lighting_command_node import LightingCommandNode
import re

number_pattern = '^(-?[0-9]+\\.?[0-9]*)$'
addition_pattern = '(\\s?\\+\\s?)'

# expression := number | operation
# operation := expression~operator~expression
# operator := multiplication | division | addition | subtraction


# https://gist.github.com/yelouafi/556e5159e869952335e01f6b473c4ec1
class NumberParser:

    def parse(self, token):
        result = re.search(number_pattern, token)
        if result is None:
            return ParseFailure("a valid number", token)
        parse_result = ParseResult(token, result.group(1))
        if '.' in parse_result.match:
            parse_result.value = float(parse_result.match)
        else:
            parse_result.value = int(parse_result.match)
        return parse_result


class AdditionParser:

    def parse(self, token):
        result = re.search(addition_pattern, token)
        if result is None:
            return ParseFailure("expr + expr", token)
        parse_result = ParseResult(token, result.group(1))
        # TODO: need to resolve left and right.  So need a global expression parser
        # parse_result.value = parse_result.left.value + parse_result.right.value
        return parse_result


class ExpressionParser:

    def __init__(self):
        self.numberParser = NumberParser();
        self.additionParser = AdditionParser();

    def parse(self, token):
        result = self.additionParser.parse(token)
        if type(result) is ParseFailure:
            return self.numberParser.parse(token)

        if result.left is not None:
            result.left = self.parse(result.left)
        if result.right is not None:
            result.right = self.parse(result.right)
        return result


def parse_expression(token):
    result = addition_parser.parse(token)
    if type(result) is ParseFailure:
        return number_parser.parse(token)

    if result.left is not None:
        result.left = parse_expression(result.left)
    if result.right is not None:
        result.right = parse_expression(result.right)
    return result


parser = ExpressionParser()
number_parser = NumberParser()
addition_parser = AdditionParser()


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

