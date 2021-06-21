from parsers.expression_parser import *
from parsers.parser_constants import CommandTypes
from parsers.time_parser import *

assignment_pattern = '^(\\s*\\=\\s*)'
comment_pattern = '^\\s*(//)'
while_pattern = '^while\\s+(.*)'
for_pattern = '^for\\s+(.*)\\s+in+\\s+(.*)'
color_string_pattern = '^(#' + hex_digit_pattern * 6 + ')$'
classic_sleep_pattern = '^sleep\\s+' + time_parameter_pattern + '$'
end_loop_scope_pattern = '^(\\})$'


def parse_combine_comment(token):
    return parse_generic(token, comment_pattern, CommandTypes.COMMENT)


def parse_combine_end_loop_scope(token):
    return parse_generic(token, end_loop_scope_pattern, CommandTypes.END_LOOP)


def parse_sleep_function(token):
    result = parse_function(token)
    if type(result) is ParseResult:
        result.result_type = CommandTypes.SLEEP
    return result


def parse_classic_sleep(token):
    result = re.search(classic_sleep_pattern, token)
    if result is None:
        return ParseFailure(token, token)

    value_str = result.group(1)
    units = result.group(2)
    value = parse_expression(value_str)
    if units == 's':
        value.value = value.value * 1000
    elif units == 'm':
        value.value = value.value * 60000

    return parse_sleep_function('sleep_ms(' + str(value.value) + ')')


def parse_combine_color_string(token):
    return parse_generic(token, color_string_pattern, CommandTypes.COLOR)


def parse_combine_for(token):
    result = re.search(for_pattern, token)
    if result is None:
        return ParseFailure(token, token)
    parse_result = ParseResult(token, result.group(1), CommandTypes.FOR)
    parse_result.var = parse_variable_identifier(result.group(1))
    parse_result.enumerable = parse_expression(result.group(2))
    return parse_result


def parse_combine_while(token):
    result = parse_generic(token, while_pattern, CommandTypes.WHILE)
    if type(result) is ParseFailure:
        return result
    result.new_scope = False
    if result.match.endswith('{'):
        result.match = result.match[:len(result.match) - 1].strip()
        result.new_scope = True
    return result


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


command_parsers = [
    parse_combine_assignment,
    parse_combine_comment,
    parse_combine_while,
    parse_combine_for,
    parse_combine_color_string,
    parse_sleep_function,
    parse_classic_sleep,
    parse_combine_end_loop_scope
]


def parse_command(token):
    return get_token(token, token, command_parsers)


def parse_assignment(token):
    return parse_generic(token, assignment_pattern, CommandTypes.ASSIGNMENT)
