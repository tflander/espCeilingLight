import pytest

from parsers.function_parser import *
from parsers.support.testing_dsl import flatten


def test_function_regex():
    result = re.match(function_pattern, 'random(0,1023)')
    assert result.group(1) == "random"
    assert result.group(2) == "0,1023"


def test_parse_function():
    result = parse_function("random(0,1023)")
    assert type(result) == CombineResult
    assert result.match[0] == "random"
    function_parameters = result.match[1]
    assert flatten(function_parameters[0]) == (0, ExpressionValueTypes.INT)
    assert flatten(function_parameters[1]) == (',', ExpressionValueTypes.COMMA)
    assert flatten(function_parameters[2]) == (1023, ExpressionValueTypes.INT)
    assert result.result_type == ExpressionValueTypes.FUNCTION


def test_not_a_function():
    result = parse_function("this is not a function")
    assert type(result) == ParseFailure
