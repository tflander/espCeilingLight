class AbstractLightingMode:

    current_mode_index = 0

    def next(self):
        self.current_mode_index += 1
        if self.current_mode_index == len(self.modes):
            self.current_mode_index = 0
        return self.current_mode()

    def current_mode(self):
        return self.modes[self.current_mode_index]


class WhiteModes(AbstractLightingMode):
    FULL = 1023
    HALF = 512
    QUARTER = 256

    modes = (FULL, HALF, QUARTER)

    def activate(self):
        print("White brightness:", self.current_mode())

    def deactivate(self):
        print("White off")


class RgbModes(AbstractLightingMode):
    RED = (1,0,0)
    YELLOW = (1,1,0)
    GREEN = (0,1,0)
    BLUE = (0,0,1)
    CYAN = (0,1,1)
    MAGENTA = (1,0,1)

    modes = (RED, YELLOW, GREEN, BLUE, CYAN, MAGENTA)

    def activate(self):
        print("RGB values:", self.current_mode())

    def deactivate(self):
        print("Color off")


class UvModes(AbstractLightingMode):
    STEADY = 60
    SLOW_STROBE = 1
    FAST_STROBE = 2

    modes = (STEADY, SLOW_STROBE, FAST_STROBE)

    def activate(self):
        print("Black Light Frequency (Strobe)", self.current_mode())

    def deactivate(self):
        print("UV off")


class Dark(AbstractLightingMode):

    modes = "X"

    def activate(self):
        print("OFF")

    def deactivate(self):
        print("still off")


