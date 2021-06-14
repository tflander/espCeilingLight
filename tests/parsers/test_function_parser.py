import pytest

from parsers.function_parser import *


def test_function_regex():
    result = re.match(function_pattern, 'random(0,1023)')
    assert result.group(1) == "random"
    assert result.group(2) == "0,1023"


@pytest.mark.skip("not ready")
def test_parse_function_parameters():
    result = parse_function_parameters("0,1023")
    x = 0


def test_parse_function():
    result = parse_function("random(0,1023)")
    assert type(result) == CombineResult
    assert result.match == ["random", "0,1023"]
    assert result.result_type == ExpressionValueTypes.FUNCTION


def test_not_a_function():
    result = parse_function("this is not a function")
    assert type(result) == ParseFailure
