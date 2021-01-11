import machine
import math, utime
from touch_button import *

from ntptime import settime

settime()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(200, 400))

led = machine.PWM(machine.Pin(2), freq=60)
led_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

adjust_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)

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
