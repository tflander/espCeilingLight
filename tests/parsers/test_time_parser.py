import pytest
from parsers.time_parser import TimeParser


@pytest.mark.parametrize("test_name, time_param, expected_val_and_unit, expected_delay_ms", [
    ("one second", "1s", [1, "s"], 1000),
    ("two seconds", "2s", [2, "s"], 2000),
    ("100 ms", "100ms", [100, "ms"], 100),
    ("2 minutes", "2m", [2, "m"], 120000),
])
def test_time_parser(test_name, time_param, expected_val_and_unit, expected_delay_ms):
    assert TimeParser.parse(time_param) == expected_val_and_unit


def test_invalid_param():
    assert TimeParser.parse("invalid time") is None
