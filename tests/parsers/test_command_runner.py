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
