import machine

class AbstractLightingMode:

    current_mode_index = 0

    FULL = 1023
    HALF = 512
    QUARTER = 256
    EIGHTH = 128

    def next(self):
        self.current_mode_index += 1
        if self.current_mode_index == len(self.modes):
            self.current_mode_index = 0
        return self.current_mode()

    def current_mode(self):
        return self.modes[self.current_mode_index]


class WhiteModes(AbstractLightingMode):

    modes = (AbstractLightingMode.FULL, AbstractLightingMode.HALF, AbstractLightingMode.QUARTER, AbstractLightingMode.EIGHTH)

    def __init__(self, white_pwm: machine.Pin):
        self.white_pwm = white_pwm

    def next_adjustment(self):
        pass

    def activate(self):
        self.white_pwm.duty(self.current_mode())

    def deactivate(self):
        self.white_pwm.duty(0)


class RgbModes(AbstractLightingMode):
    RED = (1,0,0)
    YELLOW = (1,1,0)
    GREEN = (0,1,0)
    BLUE = (0,0,1)
    CYAN = (0,1,1)
    MAGENTA = (1,0,1)

    modes = (RED, YELLOW, GREEN, BLUE, CYAN, MAGENTA)
    intensities = (AbstractLightingMode.FULL, AbstractLightingMode.HALF, AbstractLightingMode.QUARTER, AbstractLightingMode.EIGHTH)

    def __init__(self, red_pwm: machine.Pin, green_pwm: machine.Pin, blue_pwm: machine.Pin):
        self.red_pwm = red_pwm
        self.green_pwm = green_pwm
        self.blue_pwm = blue_pwm
        self.current_intensity_index = 0

    def current_intensity(self):
        return RgbModes.intensities[self.current_intensity_index];

    def next_adjustment(self):
        self.current_intensity_index += 1
        if self.current_intensity_index == len(self.intensities):
            self.current_intensity_index = 0
        return self.current_intensity()

    def activate(self):
        self.red_pwm.duty(self.current_intensity() * self.current_mode()[0])
        self.green_pwm.duty(self.current_intensity() * self.current_mode()[1])
        self.blue_pwm.duty(self.current_intensity() * self.current_mode()[2])

    def deactivate(self):
        self.red_pwm.duty(0)
        self.green_pwm.duty(0)
        self.blue_pwm.duty(0)


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


