import json


class Duties:

    def __init__(self, red=0, green=0, blue=0, white=0, ultra_violet=0):
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white
        self.ultra_violet = ultra_violet

    def __eq__(self, other):
        return self.red == other.red and \
               self.green == other.green and \
               self.blue == other.blue and \
               self.white == other.white and \
               self.ultra_violet == other.ultra_violet

    def as_json(self):
        values = json.loads("{}")
        values["Red"] = self.red
        values["Green"] = self.green
        values["Blue"] = self.blue
        values["White"] = self.white
        values["UltraViolet"] = self.ultra_violet
        return values

    def apply_deltas(self, deltas, target_color):
        self.red = self.calc_with_delta(self.red, deltas.red, target_color.red)
        self.green = self.calc_with_delta(self.green, deltas.green, target_color.green)
        self.blue = self.calc_with_delta(self.blue, deltas.blue, target_color.blue)
        self.white = self.calc_with_delta(self.white, deltas.white, target_color.white)
        self.ultra_violet = self.calc_with_delta(self.ultra_violet, deltas.ultra_violet, target_color.ultra_violet)

    def to_rounded_int(self):
        self_copy = Duties()
        self_copy.red = round(self.red)
        self_copy.green = round(self.green)
        self_copy.blue = round(self.blue)
        self_copy.white = round(self.white)
        self_copy.ultra_violet = round(self.ultra_violet)
        return self_copy

    @staticmethod
    def calc_with_delta(current_value, delta_value, target_value):
        if delta_value > 0:
            return min(current_value + delta_value, target_value)
        else:
            return max(current_value + delta_value, target_value)

    def __repr__(self):
        return str(self.as_json())
