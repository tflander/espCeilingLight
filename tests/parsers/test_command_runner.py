import pytest

from parsers.command_runner import *


def test_run_forever():
    commands = [
        "while forever {",
        "  #ff0000",
        "  sleep 1s",
        "  #00ff00",
        "  sleep 1s",
        "  #0000ff",
        "  sleep 1s",
        "}"
    ]
    run_scope = CommandScope(commands, None)
    # TODO: test that colors and sleep are in a new command scope
    x = 0


# TODO: also verify that run_forever works if the squiggly is on a new line
# TODO: also verify an error if the loop end token is not found
# TODO: also verify an error if an unmatched loop end token is found
def test_script_operations():
    commands = [
        "x = 0",
        "x = x+1",
        "x = x * 5",
        "x = x / 2",
        "x = x - 5"
    ]

    run_scope = CommandScope(commands, None)
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

    run_scope = CommandScope(commands, None)
    run_scope.step_command()
    run_scope.step_command()
    run_scope.step_command()
    run_scope.step_command()
    assert run_scope.value_for_local("answer") == 14


def test_color():
    commands = ["#aabb00"]
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    run_scope = CommandScope(commands, pwm_channels)
    run_scope.step_command()
    assert pwm_channels.red.duty() == 680
    assert pwm_channels.green.duty() == 748
    assert pwm_channels.blue.duty() == 0


def test_min_function():
    commands = ["x = min(1,2)"]
    run_scope = CommandScope(commands, None)
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 1


def test_min_function_not_enough_parameters():
    commands = ["x = min(1)"]
    run_scope = CommandScope(commands, None)
    run_scope.step_command()
    assert run_scope.runtime_error == "min(a,b) requires two parameters, found 1 in expression x = min(1)"


def test_min_function_too_many_parameters():
    commands = ["x = min(1, 2, 3)"]
    run_scope = CommandScope(commands, None)
    run_scope.step_command()
    assert run_scope.runtime_error == "min(a,b) requires two parameters, found 3 in expression x = min(1, 2, 3)"


def test_function_parameter_expressions():
    commands = [
        "x = 0",
        "y = 10",
        "z = min(x+3,y)"
    ]
    run_scope = CommandScope(commands, None)
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

    run_scope = CommandScope(commands, None)
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 0
    run_scope.step_command()
    assert run_scope.runtime_error == "variable y not found in expression x = y+1"


def test_invalid_script_parse():
    commands = [
        "x = 0",
        "this is not a script command"
    ]

    run_scope = CommandScope(commands, None)

    assert not run_scope.is_parsed
    assert run_scope.parse_error.message == [
        "Syntax Error, line 2",
        "  this is not a script command",
        "   ^"
    ]
