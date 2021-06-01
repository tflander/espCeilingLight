import pytest

from parsers.expression_parser import *
from parsers.parser_constants import LightingCommandNodeTypes, ExpressionValueTypes

parser = ExpressionParser()
number_parser = NumberParser()


def test_parse_number():
    result = parser.parse("0")
    assert result.token == "0"
    assert result.match == "0"
    assert result.left is None
    assert result.right is None


def test_parse_addition():
    result = parser.parse("1 + 2")
    assert result.token == "1 + 2"
    assert result.match == " + "
    assert result.left == "1"
    assert result.right == "2"


def test_parse_multiple_addition():
    result = parser.parse("1 + 2 + 3")
    assert result.token == "1 + 2 + 3"
    assert result.match == " + "
    assert result.left == "1"
    assert result.right == "2 + 3"


@pytest.mark.skip("TODO: test after combining parsers")
def test_parse_invalid_expression():
    result = parser.parse("this is invalid")
    assert result.position == 0
    assert result.expected == "a valid expression"
    assert result.actual == "this is invalid"


def test_number_parser_failure():
    result = number_parser.parse("not a number 123, so parse error")
    assert result.position == 0
    assert result.expected == "a valid number"
    assert result.actual == "not a number 123, so parse error"

