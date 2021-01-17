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


adjust_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)

# green = machine.PWM(machine.Pin(23), freq=60, duty=512)
# blue = machine.PWM(machine.Pin(22), freq=60, duty=512)

class LightingModes(AbstractLightingMode):
    WHITE = WhiteModes()
    RGB = RgbModes()
    UV = UvModes()
    OFF = Dark()

    modes = (WHITE, RGB, UV, OFF)

