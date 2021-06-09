from parsers.command_runner import *
from parsers.support.testing_dsl import *


def test_script_parse():
    commands = [
        "x = 0",
        "x = x+1"
    ]

    run_scope = CommandScope(commands)

    assert run_scope.is_parsed
    assert that(run_scope.parse_results[0]).is_assignment("x", 0)
    assert that(run_scope.parse_results[1]).is_assignment("x", "x+1")

# TODO: degenerate test parse for invalid script


def test_script_operations():
    commands = [
        "x = 0",
        "x = x+1",
        "x = x * 5"
    ]
    # TODO: test all operations

    run_scope = CommandScope(commands)
    assert run_scope.value_for_local("x") is None
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 0
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 1
    run_scope.step_command()
    assert run_scope.value_for_local("x") == 5


# TODO: degenerate test run for undefined variable
# TODO: degenerate test for running past end of script?
