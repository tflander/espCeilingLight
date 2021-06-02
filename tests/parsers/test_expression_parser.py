import pytest

from parsers.expression_parser import *


def test_parse_number():
    results = parse_expression("0")
    assert len(results) == 1
    assert type(results[0]) is ParseResult
    # TODO: test result of combinator


def test_parse_addition():
    results = parse_expression("1 + 2")
    assert len(results) == 3
    # TODO: test result of combinator


def test_parse_multiplication():
    results = parse_expression("2 * 3")
    assert len(results) == 3
    # TODO: test result of combinator


def test_parse_multiple_addition():
    results = parse_expression("1 + 2 + 3")
    assert len(results) == 5
    # TODO: test result of combinator


def test_parse_multiplication_with_addition():
    results = parse_expression("1 + 2 * 3 + 4")
    assert len(results) == 7
    # TODO: test result of combinator


@pytest.mark.skip("TODO: test after combining parsers.  Maybe after writing the command parser.")
def test_parse_invalid_expression():
    result = parse_expression("this is invalid")
    assert result.expected == "a valid expression"
    assert result.actual == "this is invalid"


def test_number_parser_failure():
    result = parse_number("not a number 123, so parse error")
    assert result.expected == "a valid number"
    assert result.actual == "not a number 123, so parse error"

