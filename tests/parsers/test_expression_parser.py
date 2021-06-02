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


def test_parse_invalid_expression():
    result = parse_expression("1 + 2 * 3 + 4 junk")
    assert result.line == 1
    assert result.message == [
        "Syntax Error, line 1",
        "  1 + 2 * 3 + 4 junk",
        "                ^"
    ]
