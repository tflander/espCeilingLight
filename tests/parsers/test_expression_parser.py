import pytest

from parsers.expression_parser import *


def test_parse_number():
    result = parse_expression("0")
    assert result.value == 0


def test_parse_addition():
    result = parse_expression("1    + 2")
    assert result.value == 3


def test_parse_multiplication():
    result = parse_expression("2 * 3")
    assert result.value == 6


def test_parse_division():
    result = parse_expression("10 / 2")
    assert result.value == 5


def test_parse_subtraction():
    result = parse_expression("2 - 3")
    assert result.value == -1


def test_parse_multiple_addition():
    result = parse_expression("1 + 2 + 3")
    assert result.value == 6


def test_parse_multiple_multiplication():
    result = parse_expression("2 * 3 * 4")
    assert result.value == 24


def test_parse_multiplication_with_addition():
    result = parse_expression("1 + 2 * 3 + 4")
    assert result.value == 11


def test_hex_math():
    result = parse_expression("0x0f * 10")
    assert result.value == 150


def test_variable_identifier():
    result = parse_expression("some_variableName20 * 10")
    assert result.result_type == ExpressionValueTypes.OPERATION
    assert result.left.match == "some_variableName20"
    assert result.right.value == 10


def test_complex_variable_expression():
    result = parse_expression("y * 20 / z")  # TODO: more complex, like "x * 10 + y * 20 / z"
    assert result.match == ExpressionValueTypes.DIVISION
    assert result.result_type == ExpressionValueTypes.OPERATION
    assert result.left.match == ExpressionValueTypes.MULTIPLICATION
    assert result.left.result_type == ExpressionValueTypes.OPERATION
    assert result.left.left.match == "y"
    assert result.left.left.result_type == ExpressionValueTypes.VARIABLE
    assert result.left.right.value == 20
    assert result.left.right.result_type == ExpressionValueTypes.INT
    assert result.right.match == "z"
    assert result.right.result_type == ExpressionValueTypes.VARIABLE

# TODO: parens


def test_parse_invalid_parse():
    result = parse_expression("1 + 2 * 3 + 4 junk")
    assert result.line == 1
    assert result.message == [
        "Syntax Error, line 1",
        "  1 + 2 * 3 + 4 junk",
        "                ^"
    ]


def test_parse_invalid_combine():
    result = parse_expression("1 + 2 * * 3 + 4")
    show_message(result)
    assert result.line == 1
    assert result.message == [
        "Syntax Error, line 1",
        "  1 + 2 * * 3 + 4",
        "        ^"
    ]
