from parsers.parser_constants import LightingCommandNodeTypes, ExpressionValueTypes


class LightingCommandNode:
    def __init__(self, command_node_type: LightingCommandNodeTypes, raw):
        self.type = command_node_type
        self.raw = raw
        self.value_type = self.determine_value_type()
        self.left = None;
        self.right = None;
        self.value = self.determine_value()


    def determine_value_type(self):
        if '+' in self.raw:
            return ExpressionValueTypes.ADDITION
        if '.' in self.raw:
            return ExpressionValueTypes.FLOAT
        return ExpressionValueTypes.INT

    def determine_value(self):
        if self.value_type == ExpressionValueTypes.FLOAT:
            return float(self.raw)
        elif self.value_type == ExpressionValueTypes.ADDITION:
            self.left = LightingCommandNode(None, "1")
            self.right = LightingCommandNode(None, "2")
            return self.left.value + self.right.value
        return int(self.raw)

