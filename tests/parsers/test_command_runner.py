import pytest

from parsers.command_runner import *
from parsers.support.testing_dsl import *


def test_script_operations():
    commands = [
        "x = 0",
        "x = x+1",
        "x = x * 5",
        "x = x / 2",
        "x = x - 5"
    ]

    run_scope = CommandScope(commands)
    assert run_scope.value_for_local("x") is None
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 0
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 1
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 5
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 2.5
    run_scope.step_command()
    assert run_scope.value_for_local("x") == -2.5


def test_assignment_with_parens():
    commands = [
        "x = 2",
        "y = 3",
        "z = 4",
        "answer = x * ( y + z)",
    ]

    run_scope = CommandScope(commands)
    run_scope.step_command()
    run_scope.step_command()
    run_scope.step_command()
    run_scope.step_command()
    assert run_scope.value_for_local("answer") == 14


def test_min_function():
    commands = ["x = min(1,2)"]
    run_scope = CommandScope(commands)
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 1


def test_min_function_not_enough_parameters():
    commands = ["x = min(1)"]
    run_scope = CommandScope(commands)
    run_scope.step_command()
    assert run_scope.runtime_error == "min(a,b) requires two parameters, found 1 in expression x = min(1)"


def test_min_function_too_many_parameters():
    commands = ["x = min(1, 2, 3)"]
    run_scope = CommandScope(commands)
    run_scope.step_command()
    assert run_scope.runtime_error == "min(a,b) requires two parameters, found 3 in expression x = min(1, 2, 3)"


def test_function_parameter_expressions():
    commands = [
        "x = 0",
        "y = 10",
        "z = min(x+3,y)"
    ]
    run_scope = CommandScope(commands)
    run_scope.step_command()
    run_scope.step_command()
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 0
    assert run_scope.value_for_local("y") == 10
    assert run_scope.value_for_local("z") == 3


def test_undefined_variable():
    commands = [
        "x = 0",
        "x = y+1"
    ]

    run_scope = CommandScope(commands)
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 0
    run_scope.step_command()
    assert run_scope.runtime_error == "variable y not found in expression x = y+1"


def test_invalid_script_parse():
    commands = [
        "x = 0",
        "this is not a script command"
    ]

    run_scope = CommandScope(commands)

    assert not run_scope.is_parsed
    assert run_scope.parse_error.message == [
        "Syntax Error, line 2",
        "  this is not a script command",
        "   ^"
    ]
