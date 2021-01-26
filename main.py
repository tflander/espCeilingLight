import machine
import math, utime
from touch_button import *
from lighting_modes import *

from ntptime import settime
import uasyncio

settime()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))

led = machine.PWM(machine.Pin(2), freq=4, duty=512)
led_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)


mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

red = machine.PWM(machine.Pin(21), freq=60, duty=0)
green = machine.PWM(machine.Pin(23), freq=60, duty=0)
blue = machine.PWM(machine.Pin(22), freq=60, duty=0)
white = machine.PWM(machine.Pin(19), freq=60, duty=0)
ultra_violet = machine.PWM(machine.Pin(18), freq=60, duty=0)

class LightingModes(AbstractLightingMode):
    WHITE = WhiteModes(white)
    RGB = RgbModes(red, green, blue)
    UV = UvModes(ultra_violet)
    OFF = Dark()

    # modes = (WHITE, RGB, UV, OFF)
    modes = (WHITE, RGB)

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

