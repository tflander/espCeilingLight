import pytest

from parsers.command_parser import *
from parsers.support.testing_dsl import flatten


def test_parse_variable_assignment():
    result = parse_command("x=0")

    assert flatten(result) == ("=", CommandTypes.ASSIGNMENT)
    assert flatten(result.left) == ("x", ExpressionValueTypes.VARIABLE)
    assert flatten(result.right) == (0, ExpressionValueTypes.INT)


def test_begin_while_forever_loop():
    result = parse_command("while forever")
    assert flatten(result) == ("forever", CommandTypes.WHILE)
    assert not result.new_scope


def test_begin_while_forever_loop_with_curly():
    result = parse_command("while forever {")
    assert flatten(result) == ("forever", CommandTypes.WHILE)
    assert result.new_scope


def test_end_loop_scope():
    result = parse_command("}")
    assert flatten(result) == ("}", CommandTypes.END_LOOP)


def test_begin_for_loop():
    # TODO: for now, let's defer the { } braces as a command for defining, pushing and popping a new run scope
    result = parse_command("for x in range(1, 10)")
    assert flatten(result) == ("x", CommandTypes.FOR)
    assert flatten(result.var) == ("x", ExpressionValueTypes.VARIABLE)
    assert flatten(result.enumerable) == ("range(1, 10)", ExpressionValueTypes.FUNCTION)


def test_set_color():
    result = parse_command("#aa99C0")
    assert flatten(result) == ("#aa99C0", CommandTypes.COLOR)


def test_drop_leading_spaces():
    result = parse_command("   #aa99C0")
    assert flatten(result) == ("#aa99C0", CommandTypes.COLOR)


def test_classic_sleep():
    result = parse_command("sleep 2s")
    assert flatten(result) == ("sleep_ms(2000)", CommandTypes.SLEEP)


def test_sleep_ms():
    result = parse_command("sleep_ms(1000)")
    assert flatten(result) == ("sleep_ms(1000)", CommandTypes.SLEEP)


def test_comment():
    result = parse_command("// This is a comment")
    assert flatten(result) == (CommandTypes.COMMENT, CommandTypes.COMMENT)
