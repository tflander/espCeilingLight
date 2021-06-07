import re

from parsers.parser_constants import ExpressionValueTypes

number_pattern = '^(-?[0-9]+\\.?[0-9]*)'
hex_number_pattern = '^(0x[0-9a-fA-F]+)'

left_paren_pattern = '^(\\s*\\(\\s*)'
right_paren_pattern = '^(\\s*\\)\\s*)'

addition_pattern = '^(\\s*\\+\\s*)'
multiplication_pattern = '^(\\s*\\*\\s*)'
division_pattern = '^(\\s*\\/\\s*)'
subtraction_pattern = '^(\\s*\\-\\s*)'
variable_identifier_pattern = '^([_a-zA-Z][_0-9a-zA-Z]*)'

# expression := number | variable_identifier | operation
# operation := expression~operator~expression
# operator := multiplication | addition | division | subtraction
# number := int | float | hex


def parse_number(token):
    result = parse_hex(token)
    if type(result) == ParseFailure:
        result = parse_int_or_float(token)
    return result


def parse_int_or_float(token):
    result = re.search(number_pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), None)

    if '.' in parse_result.match:
        parse_result.value = float(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.FLOAT
    else:
        parse_result.value = int(parse_result.match)
        parse_result.result_type = ExpressionValueTypes.INT
    return parse_result


def parse_hex(token):
    return parse_generic(token, hex_number_pattern, ExpressionValueTypes.HEX, lambda v: int(v, 16))


def parse_left_paren(token):
    return parse_generic(token, left_paren_pattern, ExpressionValueTypes.LEFT_PAREN)


def parse_right_paren(token):
    return parse_generic(token, right_paren_pattern, ExpressionValueTypes.RIGHT_PAREN)


def parse_variable_identifier(token):
    return parse_generic(token, variable_identifier_pattern, ExpressionValueTypes.VARIABLE)


def parse_addition(token):
    return parse_generic(token, addition_pattern, ExpressionValueTypes.ADDITION)


def parse_multiplication(token):
    return parse_generic(token, multiplication_pattern, ExpressionValueTypes.MULTIPLICATION)


def parse_division(token):
    return parse_generic(token, division_pattern, ExpressionValueTypes.DIVISION)


def parse_subtraction(token):
    return parse_generic(token, subtraction_pattern, ExpressionValueTypes.SUBTRACTION)


operation_parsers = [parse_addition, parse_multiplication, parse_division, parse_subtraction]


def parse_operation(token):
    for parser in operation_parsers:
        result = parser(token)
        if type(result) is ParseResult:
            return result
    return result


def parse_generic(token, pattern, value_type, value_resolver=None):
    result = re.search(pattern, token)
    if result is None:
        return ParseFailure(token, token, 1)
    parse_result = ParseResult(token, result.group(1), value_type)
    if value_resolver is not None:
        parse_result.value = value_resolver(parse_result.match)

    return parse_result


expression_parsers = [parse_number, parse_operation, parse_variable_identifier, parse_left_paren, parse_right_paren]


def parse_expression(original_token):
    token_results = []
    token = original_token
    while len(token) > 0:
        latest_result = None
        for parser in expression_parsers:
            result = parser(token)
            if type(result) == ParseResult:
                latest_result = result
                token = result.rest
                break
        if latest_result is None:
            return ParseFailure(token, original_token, 1)
        token_results.append(result)

    combined_results = combine_expression_results(token_results)
    if type(combined_results) == CombineFailure:
        failure = ParseFailure("", original_token, 1)

        failure.message = [
            "Syntax Error, line " + str(1),
            "  " + original_token,
            "  " + (" " * len(combined_results.errored_token)) + "^"
        ]
        return failure

    if len(combined_results) != 1:
        # TODO this happens for unexpected combine errors, such as leftover tokens
        failure = CombineFailure(original_token, 1)
        failure.message = ["unexpected combine error for token " + original_token]
        return failure
    return combined_results[0]


def combine_multiplication_results(results):
    return combine_operator_results(results, ExpressionValueTypes.MULTIPLICATION, lambda a, b: a*b)


def combine_addition_results(results):
    return combine_operator_results(results, ExpressionValueTypes.ADDITION, lambda a, b: a+b)


def combine_division_results(results):
    return combine_operator_results(results, ExpressionValueTypes.DIVISION, lambda a, b: a/b)


def combine_subtraction_results(results):
    return combine_operator_results(results, ExpressionValueTypes.SUBTRACTION, lambda a, b: a-b)


def combine_parens(results):
    for i, result in enumerate(results):
        if result.result_type == ExpressionValueTypes.LEFT_PAREN:
            left_paren_pos = i
            for j in range(len(results)-1, i, -1):
                if results[j].result_type == ExpressionValueTypes.RIGHT_PAREN:
                    inner_expression = results[left_paren_pos+1: j]
                    inner_result = combine_expression_results(inner_expression)
                    # TODO: should inner result be a list of results if can't resolve to a value?
                    return results[:left_paren_pos] + inner_result + results[j+1:], True
    return results, False


expression_combinators = [
    combine_parens,
    combine_multiplication_results,
    combine_division_results,
    combine_addition_results,
    combine_subtraction_results
]


def combine_expression_results(results):
    combined_results = results
    for combinator in expression_combinators:
        while True:
            combined_results, combined = combinator(combined_results)
            if type(combined_results) == CombineFailure:
                return combined_results
            if not combined:
                break
    return combined_results


def combine_operator_results(results, operator_value_type, value_combiner):
    for i, result in enumerate(results):
        if result.result_type == operator_value_type:
            left_operand = results[i-1]
            right_operand = results[i+1]
            token = left_operand.match + results[i].match + right_operand.match
            combined_result = ParseResult(token, operator_value_type, ExpressionValueTypes.OPERATION)

            if not is_valid_operand(left_operand) or not is_valid_operand(right_operand):
                # TODO: consider adding message about the invalid operand
                return CombineFailure(token, 1), None

            if left_operand.value is not None and right_operand.value is not None:
                combined_result.value = value_combiner(left_operand.value, right_operand.value)
            else:
                combined_result.left = left_operand
                combined_result.right = right_operand
            return results[:i-1] + [combined_result] + results[i+2:], True
    return results, False


def is_valid_operand(result):
    return result.value is not None \
        or result.result_type == ExpressionValueTypes.VARIABLE \
        or result.result_type == ExpressionValueTypes.OPERATION


class CombineResult:

    def __init__(self, token, match, result_type):
        self.result_type = result_type
        self.token = token
        self.match = match
        self.value = None


class ParseResult(CombineResult):

    def __init__(self, token, match, result_type):
        CombineResult.__init__(self, token, match, result_type)
        self.rest = token[len(match):]


class CombineFailure:

    def __init__(self, errored_token, line):
        self.errored_token = errored_token
        self.line = line


class ParseFailure(CombineFailure):
    
    def __init__(self, errored_token, text, line):
        CombineFailure.__init__(self, errored_token, line)
        pos = text.index(errored_token) + 1
        if pos > 1:
            self.message = [
                "Syntax Error, line " + str(line),
                "  " + text,
                "  " + (" " * pos) + "^"
        ]


def show_message(failure):
    for line in failure.message:
        print(line)
