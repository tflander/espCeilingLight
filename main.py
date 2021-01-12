import machine
import math, utime
from touch_button import *

from ntptime import settime

settime()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(200, 400))

led = machine.PWM(machine.Pin(2), freq=60)
led_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

adjust_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)


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


class Dark(AbstractLightingMode):

    modes = "X"

    def activate(self):
        print("OFF")


class LightingModes(AbstractLightingMode):
    WHITE = WhiteModes()
    RGB = RgbModes()
    UV = 3
    OFF = Dark()

    modes = (WHITE, RGB, UV, OFF)


def demo_modes():
    modes = LightingModes()

    def show_mode():
        current_mode = modes.current_mode()
        if type(current_mode) == int:
            print(current_mode)
        else:
            child_mode = current_mode.current_mode()
            print(current_mode, child_mode)

    show_mode()

    while True:
        mode = modes.next()
        if not type(mode) == int:
            for i in range(len(mode.modes)):
                mode.activate()
                mode.next()
        if modes.current_mode_index == 0:
            return


def two_buttons():
    while True:
        if led_touch_button.is_state_changed():
            if led_touch_button.state == TouchState.SELECTED:
                if led.duty() > 0:
                    led.duty(0)
                else:
                    led.duty(1023)
        if adjust_touch_button.is_state_changed():
            if adjust_touch_button.state == TouchState.SELECTED:
                if led.duty() > 0:
                    if led.duty() > 1000:
                        led.duty(512)
                    else:
                        led.duty(1023)
        utime.sleep_ms(20)


def activate_led_by_touch_latched():
    poll_for_touch_state_change(handle_latched_touch)


def activate_led_by_touch_momentary():
    poll_for_touch_state_change(handle_momentary_touch)


def handle_latched_touch():
    if led_touch_button.state == TouchState.SELECTED:
        if led.duty() > 0:
            led.duty(0)
        else:
            led.duty(1023)


def handle_momentary_touch():
    if led_touch_button.state == TouchState.SELECTED:
        led.duty(1023)
    elif led_touch_button.state == TouchState.RELEASED:
        led.duty(0)


def poll_for_touch_state_change(touch_handler):
    """

    :type touch_handler: function that takes no parameters and returns nothing
    """
    while True:
        if led_touch_button.is_state_changed():
            touch_handler()
        utime.sleep_ms(20)



# async def led_on(event):
#     await event.wait()
#     led.duty(1023)
#
#
# async def led_off(event):
#     await event.wait()
#     led.duty(0)


# async def toggle_led_with_uasyncio():
#
#     while True:
#         touch_selected_event = uasyncio.Event()
#         touch_release_event = uasyncio.Event()
#
#         led_on_task = uasyncio.create_task(led_on(touch_selected_event))
#         led_off_task = uasyncio.create_task(led_off(touch_release_event))
#
#         await uasyncio.sleep(1)
#         touch_selected_event.set()
#         await led_on_task
#
#         await uasyncio.sleep(1)
#         touch_release_event.set()
#         await led_off_task

# uasyncio.run(toggle_led_with_uasyncio())

# TODO: we want to eventually check last startup time to test if power was cycled twice as a reset signal.
#  The reset would put the light in normal white light mode
def timeSpike():
    print(utime.mktime(utime.localtime()) - utime.mktime((2021, 1, 4, 17, 40, 4, 0, 4)))


# def test_thread():
#     while True:
#         print("Hello from thread")
#         utime.sleep(2)


# _thread.start_new_thread(testThread, ())
