import machine


class LedPwmChannels:

    def __init__(self, red_pin, green_pin, blue_pin, white_pin, uv_pin):
        self.red = machine.PWM(machine.Pin(red_pin), freq=60, duty=0)
        self.green = machine.PWM(machine.Pin(green_pin), freq=60, duty=0)
        self.blue = machine.PWM(machine.Pin(blue_pin), freq=60, duty=0)
        self.white = machine.PWM(machine.Pin(white_pin), freq=60, duty=0)
        self.ultra_violet = machine.PWM(machine.Pin(uv_pin), freq=60, duty=0)


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


class RgbColors:
    RED = (1, 0, 0)
    YELLOW = (1, 1, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    CYAN = (0, 1, 1)
    MAGENTA = (1, 0, 1)
    BLACK = (0, 0, 0)


class WhiteModes(AbstractLightingMode):

    modes = (AbstractLightingMode.FULL, AbstractLightingMode.HALF, AbstractLightingMode.QUARTER, AbstractLightingMode.EIGHTH)
    hues = (RgbColors.BLACK, RgbColors.RED, RgbColors.BLUE)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_hue_index = 0

    def current_hue(self):
        return WhiteModes.hues[self.current_hue_index]

    def next_adjustment(self):
        self.current_hue_index += 1
        if self.current_hue_index == len(self.hues):
            self.current_hue_index = 0
        return self.current_hue()

    def activate(self):
        mode = self.current_mode()
        hue = self.current_hue()
        self.pwm_channels.white.duty(mode)
        self.pwm_channels.red.duty(mode * hue[0])
        self.pwm_channels.blue.duty(mode * hue[2])

    def deactivate(self):
        self.pwm_channels.white.duty(0)
        self.pwm_channels.red.duty(0)
        self.pwm_channels.blue.duty(0)


class RgbModes(AbstractLightingMode):

    modes = (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.BLUE, RgbColors.CYAN, RgbColors.MAGENTA)
    intensities = (AbstractLightingMode.FULL, AbstractLightingMode.HALF, AbstractLightingMode.QUARTER, AbstractLightingMode.EIGHTH)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0

    def current_intensity(self):
        return RgbModes.intensities[self.current_intensity_index];

    def next_adjustment(self):
        self.current_intensity_index += 1
        if self.current_intensity_index == len(self.intensities):
            self.current_intensity_index = 0
        return self.current_intensity()

    def activate(self):
        self.pwm_channels.red.duty(self.current_intensity() * self.current_mode()[0])
        self.pwm_channels.green.duty(self.current_intensity() * self.current_mode()[1])
        self.pwm_channels.blue.duty(self.current_intensity() * self.current_mode()[2])

    def deactivate(self):
        self.pwm_channels.red.duty(0)
        self.pwm_channels.green.duty(0)
        self.pwm_channels.blue.duty(0)


class UvModes(AbstractLightingMode):
    STEADY = 60
    SLOW_STROBE = 1
    FAST_STROBE = 2

    modes = (STEADY, SLOW_STROBE, FAST_STROBE)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels

    def activate(self):
        self.pwm_channels.ultra_violet.duty(1023)

    def deactivate(self):
        self.pwm_channels.ultra_violet.duty(0)

    def next_adjustment(self):
        pass


class Dark(AbstractLightingMode):

    modes = "X"

    def activate(self):
        print("OFF")

    def deactivate(self):
        print("still off")


