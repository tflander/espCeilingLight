import machine
import math, utime
from touch_button import *

from ntptime import settime

settime()

touch_adjust_parameters = AdjustParameters(
    max_released = 600,
    min_released = 400,
    max_selected = 200,
    min_selected = 50
)

led = machine.PWM(machine.Pin(2), freq=60)
led_touch_sensor = TouchButton(machine.Pin(4), touch_adjust_parameters)


def activate_led_by_touch_latched():
    current_state = TouchState.UNKNOWN

    while True:
        new_state = led_touch_sensor.wait_for_state_change(current_state)
        if new_state == TouchState.SELECTED:
            if led.duty() > 0:
                led.duty(0)
            else:
                led.duty(1023)
        current_state = new_state


def activate_led_by_touch_momentary():
    current_state = TouchState.UNKNOWN

    while True:
        new_state = led_touch_sensor.wait_for_state_change(current_state)
        if new_state == TouchState.SELECTED:
            led.duty(1023)
        elif new_state == TouchState.RELEASED:
            led.duty(0)
        current_state = new_state


async def led_on(event):
    await event.wait()
    led.duty(1023)


async def led_off(event):
    await event.wait()
    led.duty(0)


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


def pulse(l, t):
     for i in range(20):
         l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
         utime.sleep_ms(t)


def timeSpike():
    print(utime.mktime(utime.localtime()) - utime.mktime((2021, 1, 4, 17, 40, 4, 0, 4)))


def test_thread():
    while True:
        print("Hello from thread")
        utime.sleep(2)


# _thread.start_new_thread(testThread, ())
