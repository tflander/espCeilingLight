import pytest

from parsers.command_parser import *


def test_parse_variable_assignment():
    result = parse_command("x=0")
    assert result.result_type == ExpressionValueTypes.ASSIGNMENT
    assert result.left.result_type == ExpressionValueTypes.VARIABLE
    assert result.left.match == 'x'
    assert result.right.result_type == ExpressionValueTypes.INT
    assert result.right.value == 0
