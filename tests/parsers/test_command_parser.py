import pytest

from parsers.command_parser import *
from parsers.support.testing_dsl import flatten


def test_parse_variable_assignment():
    result = parse_command("x=0")

    assert flatten(result) == ("=", CommandTypes.ASSIGNMENT)
    assert flatten(result.left) == ("x", ExpressionValueTypes.VARIABLE)
    assert flatten(result.right) == (0, ExpressionValueTypes.INT)


def test_comment():
    result = parse_command("// This is a comment")
    assert flatten(result) == (CommandTypes.COMMENT, CommandTypes.COMMENT)
