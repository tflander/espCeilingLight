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

    assert flatten(result) == (ExpressionValueTypes.MULTIPLICATION, ExpressionValueTypes.OPERATION)
    assert flatten(result.left) == ("some_variableName20", ExpressionValueTypes.VARIABLE)
    assert flatten(result.right) == (10, ExpressionValueTypes.INT)


def test_complex_variable_expression():
    result = parse_expression("y * 20 / z")

    assert flatten(result) == (ExpressionValueTypes.DIVISION, ExpressionValueTypes.OPERATION)

    left = result.left
    assert flatten(left) == (ExpressionValueTypes.MULTIPLICATION, ExpressionValueTypes.OPERATION)
    assert flatten(left.left) == ("y", ExpressionValueTypes.VARIABLE)
    assert flatten(left.right) == (20, ExpressionValueTypes.INT)

    right = result.right
    assert flatten(right) == ("z", ExpressionValueTypes.VARIABLE)


def test_more_complex_variable_expression():
    result = parse_expression("x * 10 + y * 20 / z")

    assert flatten(result) == (ExpressionValueTypes.ADDITION, ExpressionValueTypes.OPERATION)

    left_of_addition = result.left
    assert flatten(left_of_addition) == (ExpressionValueTypes.MULTIPLICATION, ExpressionValueTypes.OPERATION)
    assert flatten(left_of_addition.left) == ("x", ExpressionValueTypes.VARIABLE)
    assert flatten(left_of_addition.right) == (10, ExpressionValueTypes.INT)

    right_of_addition = result.right
    assert flatten(right_of_addition) == (ExpressionValueTypes.DIVISION, ExpressionValueTypes.OPERATION)
    assert flatten(right_of_addition.left) == (ExpressionValueTypes.MULTIPLICATION, ExpressionValueTypes.OPERATION)

    assert flatten(right_of_addition.left.left) == ('y', ExpressionValueTypes.VARIABLE)
    assert flatten(right_of_addition.left.right) == (20, ExpressionValueTypes.INT)

    assert flatten(right_of_addition.right) == ('z', ExpressionValueTypes.VARIABLE)

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


def flatten(result):
    if result.value is not None:
        return result.value, result.result_type

    return result.match, result.result_type
