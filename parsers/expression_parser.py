from parsers.lighting_command_node import LightingCommandNode
import re

number_pattern = '^(-?[0-9]+\\.?[0-9]*)$'
addition_pattern = '(\\s?\\+\\s?)'


# https://gist.github.com/yelouafi/556e5159e869952335e01f6b473c4ec1
class NumberParser:

    def parse(self, token):
        result = re.search(number_pattern, token)
        if result is None:
            return ParseFailure("a valid number", token)
        return ParseResult(token, result.group(1))


class AdditionParser:

    def parse(self, token):
        result = re.search(addition_pattern, token)
        if result is None:
            return ParseFailure("expr + expr", token)
        return ParseResult(token, result.group(1))


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


class ParseResult:

    def __init__(self, token, match):
        self.token = token
        self.match = match
        self.left = None
        self.right = None
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
