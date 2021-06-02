import pytest

from parsers.expression_parser import *


def test_parse_number():
    result = parse_expression("0")
    assert result.value == 0


def test_parse_addition():
    result = parse_expression("1 + 2")
    assert result.value == 3


def test_parse_multiplication():
    result = parse_expression("2 * 3")
    assert result.value == 6


def test_parse_multiple_addition():
    result = parse_expression("1 + 2 + 3")
    assert result.value == 6


def test_parse_multiple_multiplication():
    result = parse_expression("2 * 3 * 4")
    assert result.value == 24


def test_parse_multiplication_with_addition():
    result = parse_expression("1 + 2 * 3 + 4")
    assert result.value == 11


@pytest.mark.skip("rescue after building the combinator")
def test_parse_invalid_expression():
    result = parse_expression("1 + 2 * 3 + 4 junk")
    assert result.line == 1
    assert result.message == [
        "Syntax Error, line 1",
        "  1 + 2 * 3 + 4 junk",
        "                ^"
    ]
