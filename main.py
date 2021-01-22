import machine
import math, utime
from touch_button import *
from lighting_modes import *

from ntptime import settime
import uasyncio

settime()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(200, 400))

led = machine.PWM(machine.Pin(2), freq=4, duty=512)
led_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)


mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

red = machine.PWM(machine.Pin(21), freq=60, duty=16)
green = machine.PWM(machine.Pin(23), freq=60, duty=512)
blue = machine.PWM(machine.Pin(22), freq=60, duty=16)
white = machine.PWM(machine.Pin(19), freq=60, duty=16)
ultra_violet = machine.PWM(machine.Pin(18), freq=60, duty=16)

class LightingModes(AbstractLightingMode):
    WHITE = WhiteModes()
    RGB = RgbModes()
    UV = UvModes()
    OFF = Dark()

    modes = (WHITE, RGB, UV, OFF)

