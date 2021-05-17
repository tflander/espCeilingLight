class LightingScriptParser:
    def parse(self, candidate_command):
        return LightingCommandNode(LightingCommandNodeTypes.EXPR, candidate_command)


class LightingCommandNodeTypes:
    EXPR = 1


class ExpressionValueTypes:
    INT = 1,
    FLOAT = 2


class LightingCommandNode:
    def __init__(self, command_node_type: LightingCommandNodeTypes, raw):
        self.type = command_node_type
        self.raw = raw
        self.value_type = self.determine_value_type()
        self.value = self.determine_value()

    def determine_value_type(self):
        if '.' in self.raw:
            return ExpressionValueTypes.FLOAT
        return ExpressionValueTypes.INT

    def determine_value(self):
        if self.value_type == ExpressionValueTypes.FLOAT:
            return float(self.raw)
        return int(self.raw)


parser = LightingScriptParser()


def test_parse_0():
    command_tree = parser.parse("0")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "0"
    assert command_tree.value_type == ExpressionValueTypes.INT
    assert command_tree.value == 0


def test_parse_3_14():
    command_tree = parser.parse("3.14")
    assert command_tree.type == LightingCommandNodeTypes.EXPR
    assert command_tree.raw == "3.14"
    assert command_tree.value_type == ExpressionValueTypes.FLOAT
    assert command_tree.value == 3.14


