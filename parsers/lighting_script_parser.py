from parsers.lighting_command_node import LightingCommandNode
from parsers.parser_constants import LightingCommandNodeTypes


class LightingScriptParser:
    def parse(self, candidate_command):
        # TODO: for now, assume expression
        return LightingCommandNode(LightingCommandNodeTypes.EXPR, candidate_command)

