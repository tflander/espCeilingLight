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


class LightingModes(AbstractLightingMode):
    WHITE = WhiteModes(led_pwm_channels)
    RGB = RgbModes(led_pwm_channels)
    UV = UvModes(led_pwm_channels)
    Party = PartyModes(led_pwm_channels)
    OFF = Dark()

    modes = (WHITE, RGB, UV, Party)  # for now, no OFF mode so I don't burn the house down.


lights = LightingModes()
lights.current_mode().activate()

while True:
    if mode_touch_button.is_state_changed():
        if mode_touch_button.state == TouchState.SELECTED:
            lights.current_mode().deactivate()
            lights.next()
            lights.current_mode().activate()

    if sub1_touch_button.is_state_changed():
        if sub1_touch_button.state == TouchState.SELECTED:
            lights.current_mode().deactivate()
            lights.current_mode().next()
            lights.current_mode().activate()

    if sub2_touch_button.is_state_changed():
        if sub2_touch_button.state == TouchState.SELECTED:
            lights.current_mode().deactivate()
            lights.current_mode().next_adjustment()
            lights.current_mode().activate()

