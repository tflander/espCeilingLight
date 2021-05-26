from parsers.lighting_script_parser import LightingScriptParser
from parsers.parser_constants import LightingCommandNodeTypes, ExpressionValueTypes

parser = LightingScriptParser()


def test_parse_0():
    command_tree = parser.parse("0")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "0"
    assert command_tree.value_type == ExpressionValueTypes.INT
    assert command_tree.value == 0


def test_parse_3_14():
    command_tree = parser.parse("3.14")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "3.14"
    assert command_tree.value_type == ExpressionValueTypes.FLOAT
    assert command_tree.value == 3.14


def test_parse_with_spaces_stripped():
    command_tree = parser.parse("  3.14  ")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "  3.14  "
    assert command_tree.value_type == ExpressionValueTypes.FLOAT
    assert command_tree.value == 3.14


def test_parse_addition_of_constants():
    command_tree = parser.parse("1+2")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "1+2"
    assert command_tree.value_type == ExpressionValueTypes.ADDITION
    assert command_tree.value == 3
    assert command_tree.left.value == 1
    assert command_tree.right.value == 2


# TODO: skip test until I understand parser combinators
def skip_test_parse_addition_of_multiple_constants():
    command_tree = parser.parse("1+2+3")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "1+2+3"
    assert command_tree.value_type == ExpressionValueTypes.ADDITION
    assert command_tree.value == 6
    assert command_tree.left.value_type == ExpressionValueTypes.ADDITION
    assert command_tree.right.value == 3

