from parsers.command_parser import parse_command


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

    # local_variables = {}
    # command_pointer = 0
    #
    # def step_command(self):
    #     pass
    #
    # def value_for_local(self, variable_name):
    #     pass
