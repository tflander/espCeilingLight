from parsers.command_runner import run_command, CommandScope
from parsers.parser_constants import CommandTypes


def test_foo():
    commands = [
        "x = 0",
        "x = x+1"
    ]

    run_scope = CommandScope(commands)
    assert run_scope.is_parsed
    assert run_scope.parse_results[0].result_type == CommandTypes.ASSIGNMENT
    # TODO: left == var x, right = int 0
    # TODO: more test helpers in poorly named flatten.py
    assert run_scope.parse_results[1].result_type == CommandTypes.ASSIGNMENT
