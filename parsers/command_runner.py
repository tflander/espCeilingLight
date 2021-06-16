from parsers.command_parser import parse_command
from parsers.parser_constants import ExpressionValueTypes
from parsers.result_objects import ParseFailure


def run_command(commands):
    pass


class CommandScope:

    def __init__(self, commands):
        self.commands = commands
        self.is_parsed = False
        self.parse_results = []

        for i, command in enumerate(commands, start=1):
            result = parse_command(command)
            self.parse_results.append(result)
            if type(result) == ParseFailure:
                self.parse_error = ParseFailure(result.errored_token, command, i)
                return

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
            if command.right.value is None:
                self.resolve_expression(command.right)
            if type(command.right.value) is str:
                # TODO: is this dead code?
                self.runtime_error = command.right.value + ' ' + "in expression " + self.commands[self.command_pointer]
                return
            self.local_variables[var_name] = command.right.value

        self.command_pointer += 1

    def resolve_function(self, result):
        parameters = result.function_parameters
        for parameter in parameters:
            self.resolve_variables(parameter)
            if parameter.value is None:
                self.resolve_expression(parameter)

        if result.function_name == 'min':
            # TODO: require two parameters
            result.value = min(parameters[0].value, parameters[1].value)

    def resolve_variables(self, result):
        if result.result_type in [ExpressionValueTypes.INT, ExpressionValueTypes.FLOAT]:
            return
        if result.result_type == ExpressionValueTypes.FUNCTION:
            self.resolve_function(result)
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
        result.value = self.resolve_operator(operator, result.left.value, result.right.value)

    def resolve_operand(self, result):
        if result.result_type == ExpressionValueTypes.OPERATION:
            self.resolve_expression(result)

    @staticmethod
    def resolve_operator(operator, left_operand, right_operand):
        # TODO: is this dead code?
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
