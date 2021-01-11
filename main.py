import machine
import math, time, utime
import _thread
from array import array
import uasyncio

from ntptime import settime

settime()

led = machine.PWM(machine.Pin(2), freq=60)

# adjust parameters for the touch sensor
max_released = 600
min_released = 400
max_selected = 200
min_selected = 50

async def led_on(event):
    await event.wait()
    led.duty(1023)


async def led_off(event):
    await event.wait()
    led.duty(0)


async def toggle_led_with_uasyncio():

    while True:
        touch_selected_event = uasyncio.Event()
        touch_release_event = uasyncio.Event()

        led_on_task = uasyncio.create_task(led_on(touch_selected_event))
        led_off_task = uasyncio.create_task(led_off(touch_release_event))

        await uasyncio.sleep(1)
        touch_selected_event.set()
        await led_on_task

        await uasyncio.sleep(1)
        touch_release_event.set()
        await led_off_task

# uasyncio.run(toggle_led_with_uasyncio())


def pulse(l, t):
     for i in range(20):
         l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
         time.sleep_ms(t)

def timeSpike():
    print(utime.mktime(utime.localtime()) - utime.mktime((2021, 1, 4, 17, 40, 4, 0, 4)))

touch = machine.TouchPad(machine.Pin(4))

def sample_touch():
    samples = list()
    for i in range(200):
        samples.append(touch.read())
        time.sleep_ms(20)

    print("max = ", max(samples))
    print("min = ", min(samples))
    print("avg = ", sum(samples) / len(samples))

def show_touch():
    while True:
        print(touch.read())
        time.sleep_ms(200)


class TouchState:
    UNKNOWN = 1
    RELEASED = 2
    SELECTED = 3
    DEAD_BAND = 4
    OUT_OF_RANGE = 5


def activate_led_by_touch_latched():
    current_state = TouchState.UNKNOWN
    is_led_on = False

    while True:
        new_state = wait_for_touch_state_change(current_state)
        if new_state == TouchState.SELECTED:
            if is_led_on:
                led.duty(0)
                is_led_on = False
            else:
                led.duty(1023)
                is_led_on = True
        current_state = new_state


def activate_led_by_touch_momentary():
    current_state = TouchState.UNKNOWN

    while True:
        new_state = wait_for_touch_state_change(current_state)
        if new_state == TouchState.SELECTED:
            led.duty(1023)
        elif new_state == TouchState.RELEASED:
            led.duty(0)
        current_state = new_state


def wait_for_touch_state_change(current_state):
    while True:
        s = touch.read()
        if min_released < s < max_released:
            new_state = TouchState.RELEASED
        elif min_selected < s < max_selected:
            new_state = TouchState.SELECTED
        elif s < min_selected or s > max_released:
            new_state = TouchState.OUT_OF_RANGE
        else:
            new_state = TouchState.DEAD_BAND

        if new_state != current_state:
            return new_state
        time.sleep_ms(20)

def testThread():
    while True:
        print("Hello from thread")
        time.sleep(2)


# _thread.start_new_thread(testThread, ())
