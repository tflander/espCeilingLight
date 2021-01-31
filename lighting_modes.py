import machine
from lighting_support import *


class WhiteModes:

    intensities = (
        AvailableIntensities.FULL,
        AvailableIntensities.HALF,
        AvailableIntensities.QUARTER,
        AvailableIntensities.EIGHTH
    )

    hues = (RgbColors.BLACK, RgbColors.RED, RgbColors.BLUE)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_hue_index = 0
        self.intensities_index = 0

    def current_hue(self):
        return WhiteModes.hues[self.current_hue_index]

    def current_intensity(self):
        return self.intensities[self.intensities_index]

    def next_hue(self):
        self.current_hue_index += 1
        if self.current_hue_index == len(self.hues):
            self.current_hue_index = 0
        return self.current_hue()

    def next_brightness_or_speed(self):
        self.intensities_index += 1
        if self.intensities_index == len(self.intensities):
            self.intensities_index = 0

    async def activate(self):
        intensity = self.current_intensity()
        hue = self.current_hue()
        self.pwm_channels.white.duty(intensity)
        self.pwm_channels.red.duty(intensity * hue[0])
        self.pwm_channels.blue.duty(intensity * hue[2])

    def deactivate(self):
        self.pwm_channels.white.duty(0)
        self.pwm_channels.red.duty(0)
        self.pwm_channels.blue.duty(0)


class RgbModes:

    colors = (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.BLUE, RgbColors.CYAN, RgbColors.MAGENTA)
    modes = (
        AvailableIntensities.FULL,
        AvailableIntensities.HALF,
        AvailableIntensities.QUARTER,
        AvailableIntensities.EIGHTH
    )

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_color_index = 0

    def current_color(self):
        return RgbModes.colors[self.current_color_index];

    def next_adjustment(self):
        self.current_color_index += 1
        if self.current_color_index == len(self.colors):
            self.current_color_index = 0
        return self.current_color()

    def activate(self):
        self.pwm_channels.red.duty(self.current_mode() * self.current_color()[0])
        self.pwm_channels.green.duty(self.current_mode() * self.current_color()[1])
        self.pwm_channels.blue.duty(self.current_mode() * self.current_color()[2])

    def deactivate(self):
        self.pwm_channels.red.duty(0)
        self.pwm_channels.green.duty(0)
        self.pwm_channels.blue.duty(0)



