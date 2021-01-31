import machine
import math, utime
from touch_button import *
from lighting_modes import *
from party import *

from ntptime import settime
import uasyncio

settime()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))

mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)


def control_lighting():
    party_modes = LightModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    party_modes.activate()

    while True:

        selected_button = await button_collection.wait_for_button_select()

        party_modes.deactivate()
        if selected_button == 0:
            party_modes.next_mode()
        elif selected_button == 1:
            party_modes.next_hue()
        else:
            party_modes.next_brightness_or_speed()
        party_modes.activate()
        uasyncio.sleep_ms(10)


class LightModes:

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None
        self.current_mode_index = 0

        self.modes = (
            WhiteModes(self.pwm_channels),
            MultiColorFlash(self.pwm_channels, (
                (RgbColors.RED, RgbColors.BLUE),
                (RgbColors.BLUE, RgbColors.YELLOW),
                (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.CYAN, RgbColors.BLUE, RgbColors.MAGENTA)
            )),
            OneColorGlow(self.pwm_channels, (
                RgbColors.RED,
                RgbColors.GREEN,
                RgbColors.BLUE,
                RgbColors.CYAN,
                RgbColors.YELLOW,
                RgbColors.MAGENTA)
            )
        )

    def current_mode(self):
        return self.modes[self.current_mode_index]

    def activate(self):
        self.task = uasyncio.create_task(self.current_mode().activate())

    def next_mode(self):
        self.current_mode_index += 1
        if self.current_mode_index == len(self.modes):
            self.current_mode_index = 0

    def next_hue(self):
        self.current_mode().next_hue()

    def next_brightness_or_speed(self):
        self.current_mode().next_brightness_or_speed()

    def deactivate(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None
        led_pwm_channels.zero_duty()


print("running lights")
uasyncio.run(control_lighting())
