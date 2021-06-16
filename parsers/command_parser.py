from parsers.expression_parser import *
from parsers.parser_constants import CommandTypes

assignment_pattern = '^(\\s*\\=\\s*)'
comment_pattern = '^\\s*(//)'
while_pattern = '^while\\s+(.*)'
for_pattern = '^for\\s+(.*)\\s+in+\\s+(.*)'


def parse_combine_comment(token):
    return parse_generic(token, comment_pattern, CommandTypes.COMMENT)


def parse_combine_for(token):
    result = re.search(for_pattern, token)
    if result is None:
        return ParseFailure(token, token)
    parse_result = ParseResult(token, result.group(1), CommandTypes.FOR)
    parse_result.var = parse_variable_identifier(result.group(1))
    parse_result.enumerable = parse_expression(result.group(2))
    return parse_result


def parse_combine_while(token):
    return parse_generic(token, while_pattern, CommandTypes.WHILE)


def parse_combine_assignment(token):
    variable = parse_variable_identifier(token)
    if type(variable) is ParseFailure:
        return variable
    assignment = parse_assignment(variable.rest)
    if type(assignment) is ParseFailure:
        return assignment
    rhs = parse_expression(assignment.rest)
    assignment.left = variable
    assignment.right = rhs
    return assignment


command_parsers = [parse_combine_assignment, parse_combine_comment, parse_combine_while, parse_combine_for]


def parse_command(token):
    return get_token(token, token, command_parsers)


def parse_assignment(token):
    return parse_generic(token, assignment_pattern, CommandTypes.ASSIGNMENT)
