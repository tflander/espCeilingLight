# TODO: move abstract stuff to a different library
from lighting_modes import *


class PartyModes(AbstractLightingMode):

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0

    def activate(self):
        self.pwm_channels.red.duty(1023)  # stub for now

    # TODO: generic deactivate in super-class
    def deactivate(self):
        self.pwm_channels.red.duty(0)
        self.pwm_channels.green.duty(0)
        self.pwm_channels.blue.duty(0)
