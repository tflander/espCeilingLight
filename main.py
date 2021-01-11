import machine
import math, time, utime
import _thread
from array import array

from ntptime import settime

settime()

led = machine.PWM(machine.Pin(2), freq=60)

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


def touch_state():
    current_state = TouchState.UNKNOWN
    max_released = 600
    min_released = 400
    max_selected = 200
    min_selected = 50
    counter = 0
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
            counter += 1
            current_state = new_state
            print(new_state)

        time.sleep_ms(20)

def testThread():
    while True:
        print("Hello from thread")
        time.sleep(2)


# _thread.start_new_thread(testThread, ())
