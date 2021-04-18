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

    def __repr__(self):
        return str(self.as_json())
