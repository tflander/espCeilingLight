class Presets:

    def __init__(self):
        self.presets = []
        self.current_preset = -1

    @staticmethod
    def select_next_preset():
        pass

    def add(self, commands):
        self.presets.append(commands)

    def next(self):
        self.current_preset += 1
        if self.current_preset >= len(self.presets):
            self.current_preset = 0
        return self.presets[self.current_preset]
