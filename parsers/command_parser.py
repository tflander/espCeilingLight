from parsers.expression_parser import *
from parsers.parser_constants import CommandTypes

assignment_pattern = '^(\\s*\\=\\s*)'


def parse_command(token):
    result = parse_combine_assignment(token)
    if type(result) == ParseFailure:
        result = parse_combine_comment(token)
    return result


def parse_combine_comment(token):
    pass  # TODO: stuffis


def parse_combine_assignment(token):
    variable = parse_variable_identifier(token)
    if type(variable) is not ParseFailure:
        assignment = parse_assignment(variable.rest)
        rhs = parse_expression(assignment.rest)
        assignment.left = variable
        assignment.right = rhs
        return assignment

    return variable


def parse_assignment(token):
    return parse_generic(token, assignment_pattern, CommandTypes.ASSIGNMENT)
