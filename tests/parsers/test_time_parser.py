import pytest

from parsers.parser_constants import ExpressionValueTypes
from parsers.support.testing_dsl import flatten
from parsers.time_parser import parse_classic_time


@pytest.mark.parametrize("test_name, time_param, expected_val_and_unit, expected_delay_ms", [
    ("one second", "1s", [1, "s"], 1000),
    ("two seconds", "2s", [2, "s"], 2000),
    ("100 ms", "100ms", [100, "ms"], 100),
    ("2 minutes", "2m", [2, "m"], 120000),
])
def test_time_parser(test_name, time_param, expected_val_and_unit, expected_delay_ms):
    assert flatten(parse_classic_time(time_param)) == (expected_delay_ms, ExpressionValueTypes.TIME)


def test_invalid_param():
    result = parse_classic_time("10x")
    assert result.errored_token == '10x'
    assert result.message == ['Syntax Error', '  10x', '   ^']
