from parsers.command_parser import parse_command
from parsers.parser_constants import ExpressionValueTypes


def run_command(commands):
    pass


class CommandScope:

    def __init__(self, commands):
        self.commands = commands
        self.is_parsed = False
        self.parse_results = []

        for command in commands:
            result = parse_command(command)
            self.parse_results.append(result)

        self.is_parsed = True

        self.local_variables = {}
        self.command_pointer = 0

    def step_command(self):
        command = self.parse_results[self.command_pointer]
        var_name = command.left.match
        if command.right.value is not None:
            value = command.right.value
        else:
            value = self.resolve_expression(command.right)
        self.local_variables[var_name] = value

        self.command_pointer += 1

    def value_for_local(self, variable_name):
        if variable_name not in self.local_variables:
            return None
        return self.local_variables[variable_name]

    def resolve_expression(self, result):
        operator = result.match
        left_operand = self.resolve_operand(result.left)
        right_operand = self.resolve_operand(result.right)
        return self.resolve_operator(operator, left_operand, right_operand)

    def resolve_operand(self, result):
        if result.value is not None:
            return result.value
        else:
            if result.match in self.local_variables:
                return self.local_variables[result.match]
            else:
                return "whoopsie-poopsie"

    @staticmethod
    def resolve_operator(operator, left_operand, right_operand):
        if type(left_operand) == str:
            return left_operand
        if type(right_operand) == str:
            return right_operand
        if operator == ExpressionValueTypes.ADDITION:
            return left_operand + right_operand
        elif operator == ExpressionValueTypes.MULTIPLICATION:
            return left_operand * right_operand
        elif operator == ExpressionValueTypes.DIVISION:
            return left_operand / right_operand
        elif operator == ExpressionValueTypes.SUBTRACTION:
            return left_operand - right_operand
