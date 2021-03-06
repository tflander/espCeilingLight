import pytest

from parsers.expression_parser import *
from parsers.support.testing_dsl import flatten


def test_function_regex():
    result = re.match(function_pattern, 'random(0,1023)')
    assert result.group(1) == "random"
    assert result.group(2) == "0,1023"


def test_parse_function():
    result = parse_function("random(0,1023)")
    assert result.function_name == "random"
    assert flatten(result.function_parameters[0]) == (0, ExpressionValueTypes.INT)
    assert flatten(result.function_parameters[1]) == (1023, ExpressionValueTypes.INT)
    assert result.result_type == ExpressionValueTypes.FUNCTION


def test_parse_function_parameter_expressions():
    result = parse_function("random(x+1,1023)")
    assert result.function_name == "random"
    assert result.result_type == ExpressionValueTypes.FUNCTION
    assert flatten(result.function_parameters[0]) == (ExpressionValueTypes.ADDITION, ExpressionValueTypes.OPERATION)
    assert flatten(result.function_parameters[0].left) == ('x', ExpressionValueTypes.VARIABLE)
    assert flatten(result.function_parameters[0].right) == (1, ExpressionValueTypes.INT)
    assert flatten(result.function_parameters[1]) == (1023, ExpressionValueTypes.INT)


def test_parse_function_one_parameter():
    result = parse_function("sleep_ms(1000)")
    assert result.function_name == "sleep_ms"
    assert result.result_type == ExpressionValueTypes.FUNCTION
    assert flatten(result.function_parameters[0]) == (1000, ExpressionValueTypes.INT)


def test_parse_function_no_parameter():
    result = parse_function("random()")
    assert result.function_name == "random"
    assert result.result_type == ExpressionValueTypes.FUNCTION
    assert len(result.function_parameters) == 0


def test_parse_function_invalid_parameter_list():
    result = parse_function("random(0, 1023, )")
    assert type(result) == ParseFailure
    assert result.message == [
        'Syntax Error',
        '  random(0, 1023, )',
        '   ^'
    ]


def test_parse_function_invalid_parameter():
    result = parse_function("random(0:1023)")
    assert type(result) == ParseFailure
    assert result.message == [
        'Syntax Error',
        '  random(0:1023)',
        '           ^'
    ]


def test_not_a_function():
    result = parse_function("this is not a function")
    assert type(result) == ParseFailure
