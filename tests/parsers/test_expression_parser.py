import pytest

from parsers.expression_parser import *
from parsers.parser_constants import LightingCommandNodeTypes, ExpressionValueTypes


def test_parse_number():
    result = parse_expression("0")
    assert result.token == "0"
    assert result.match == "0"
    assert result.left is None
    assert result.right is None
    assert result.value == 0


def test_parse_addition():
    result = parse_expression("1 + 2")
    assert result.token == "1 + 2"
    assert result.match == " + "
    assert result.left.match == "1"
    assert result.right.match == "2"
    assert result.value == 3


# TODO: clean up test
def test_parse_multiple_addition():
    result = parse_expression("1 + 2 + 3")
    assert result.token == "1 + 2 + 3"
    assert result.match == " + "
    assert result.left.match == "1"
    assert result.right.match == " + "
    assert result.value == 6


@pytest.mark.skip("TODO: test after combining parsers.  Maybe after writing the command parser.")
def test_parse_invalid_expression():
    result = parse_expression("this is invalid")
    assert result.expected == "a valid expression"
    assert result.actual == "this is invalid"


def test_number_parser_failure():
    result = parse_number("not a number 123, so parse error")
    assert result.expected == "a valid number"
    assert result.actual == "not a number 123, so parse error"

