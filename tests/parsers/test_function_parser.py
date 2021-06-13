import pytest

from parsers.function_parser import *
from parsers.support.testing_dsl import flatten


def test_function_regex():
    result = re.match(function_pattern, 'random(0,1023)')
    assert result.group(1) == "random"
    assert result.group(2) == "0,1023"


def test_parse_function():
    result = parse_function("random(0,1023)");
    assert type(result) == CombineResult
    assert result.match == ["random", "0,1023"]
    assert result.result_type == ExpressionValueTypes.FUNCTION
