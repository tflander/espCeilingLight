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
        self.runtime_error = None

    def step_command(self):
        if self.runtime_error is not None:
            return
        command = self.parse_results[self.command_pointer]
        # TODO: this assumes assignment, which is currently the only command
        var_name = command.left.match
        self.resolve_variables(command.right)
        if self.runtime_error is not None:
            self.runtime_error = self.runtime_error + ' ' + "in expression " + self.commands[self.command_pointer]
            return
        else:
            value = command.right.value
            if value is None:
                value = self.resolve_expression(command.right)
            if type(value) is str:
                # TODO: is this dead code?
                self.runtime_error = value + ' ' + "in expression " + self.commands[self.command_pointer]
                return
            self.local_variables[var_name] = value

        self.command_pointer += 1

    def resolve_variables(self, result):
        if result.result_type in [ExpressionValueTypes.INT, ExpressionValueTypes.FLOAT]:
            return
        if result.result_type == ExpressionValueTypes.VARIABLE:
            if result.match in self.local_variables:
                result.value = self.local_variables[result.match]
                return
            else:
                self.runtime_error = "variable " + result.match + " not found"
                return
        self.resolve_variables(result.left)
        self.resolve_variables(result.right)

    def value_for_local(self, variable_name):
        if variable_name not in self.local_variables:
            return None
        return self.local_variables[variable_name]

    def resolve_expression(self, result):
        operator = result.match
        self.resolve_operand(result.left)
        self.resolve_operand(result.right)
        return self.resolve_operator(operator, result.left.value, result.right.value)

    def resolve_operand(self, result):
        if result.result_type == ExpressionValueTypes.OPERATION:
            self.resolve_expression(result)

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
