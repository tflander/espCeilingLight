from parsers.expression_parser import *

assignment_pattern = '^(\\s*\\=\\s*)'


def parse_command(token):
    variable = parse_variable_identifier(token)
    assignment = parse_assignment(variable.rest)
    rhs = parse_expression(assignment.rest)
    assignment.left = variable
    assignment.right = rhs
    return assignment


def parse_assignment(token):
    return parse_generic(token, assignment_pattern, ExpressionValueTypes.ASSIGNMENT)
