import pytest

from parsers.command_parser import *
from parsers.support.testing_dsl import flatten


def test_parse_variable_assignment():
    result = parse_command("x=0")

    assert flatten(result) == ("=", CommandTypes.ASSIGNMENT)
    assert flatten(result.left) == ("x", ExpressionValueTypes.VARIABLE)
    assert flatten(result.right) == (0, ExpressionValueTypes.INT)


def test_begin_while_forever_loop():
    # TODO: for now, let's defer the { } braces as a command for defining, pushing and popping a new run scope
    result = parse_command("while forever")
    assert flatten(result) == ("forever", CommandTypes.WHILE)


def test_comment():
    result = parse_command("// This is a comment")
    assert flatten(result) == (CommandTypes.COMMENT, CommandTypes.COMMENT)
