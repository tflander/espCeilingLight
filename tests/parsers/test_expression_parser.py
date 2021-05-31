import pytest

from parsers.expression_parser import *
from parsers.parser_constants import LightingCommandNodeTypes, ExpressionValueTypes

parser = ExpressionParser()
number_parser = NumberParser()


def test_parse_number():
    result = parser.parse("0")
    assert result.token == "0"
    assert result.match == "0"
    assert result.left is None
    assert result.right is None


@pytest.mark.skip("TODO: test after combining parsers")
def test_parse_invalid_expression():
    result = parser.parse("this is invalid")
    assert result.position == 0
    assert result.expected == "a valid expression"
    assert result.actual == "this is invalid"


def test_number_parser_failure():
    result = number_parser.parse("not a number 123, so parse error")
    assert result.position == 0
    assert result.expected == "a valid number"
    assert result.actual == "not a number 123, so parse error"

# def test_parse_3_14():
#     command_tree = parser.parse("3.14")
#     assert command_tree.type == LightingCommandNodeTypes.EXPR
#     assert command_tree.raw == "3.14"
#     assert command_tree.value_type == ExpressionValueTypes.FLOAT
#     assert command_tree.value == 3.14
#
#
# def test_parse_with_spaces_stripped():
#     command_tree = parser.parse("  3.14  ")
#     assert command_tree.type == LightingCommandNodeTypes.EXPR
#     assert command_tree.raw == "  3.14  "
#     assert command_tree.value_type == ExpressionValueTypes.FLOAT
#     assert command_tree.value == 3.14
#
#
# def test_parse_addition_of_constants():
#     command_tree = parser.parse("1+2")
#     assert command_tree.type == LightingCommandNodeTypes.EXPR
#     assert command_tree.raw == "1+2"
#     assert command_tree.value_type == ExpressionValueTypes.ADDITION
#     assert command_tree.value == 3
#     assert command_tree.left.value == 1
#     assert command_tree.right.value == 2
#
#
# # TODO: skip test until I understand parser combinators
# def skip_test_parse_addition_of_multiple_constants():
#     command_tree = parser.parse("1+2+3")
#     assert command_tree.type == LightingCommandNodeTypes.EXPR
#     assert command_tree.raw == "1+2+3"
#     assert command_tree.value_type == ExpressionValueTypes.ADDITION
#     assert command_tree.value == 6
#     assert command_tree.left.value_type == ExpressionValueTypes.ADDITION
#     assert command_tree.right.value == 3
#
