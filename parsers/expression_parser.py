from parsers.lighting_command_node import LightingCommandNode
import re

number_pattern = '^(-?[0-9]+\\.?[0-9]*)'
addition_pattern = '(\\s?\\+\\s?)'


# https://gist.github.com/yelouafi/556e5159e869952335e01f6b473c4ec1
class NumberParser:

    def parse(self, token):
        result = re.match(number_pattern, token)
        if result is None:
            return ParseFailure(0, "a valid number", token)
        return ParseResult(token, result.group(1))


class ExpressionParser:

    def __init__(self):
        self.numberParser = NumberParser();

    def parse(self, token):
        return self.numberParser.parse(token)


class ParseResult:

    def __init__(self, token, match):
        self.token = token
        self.match = match
        self.left = None
        self.right = None
        candidate_right = token[token.find(match) + len(match):].strip()
        if len(candidate_right) > 0:
            self.right = candidate_right


class ParseFailure:
    
    def __init__(self, position, expected, actual):
        self.actual = actual
        self.expected = expected
        self.position = position
