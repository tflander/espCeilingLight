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

    while True:
        new_state = TouchState.UNKNOWN
        s = touch.read()
        if min_released < s < max_released:
            new_state = TouchState.RELEASED
        elif min_selected < s < max_selected:
            new_state = TouchState.SELECTED
        elif s < min_selected or s > max_selected:
            new_state = TouchState.DEAD_BAND
        else:
            new_state = TouchState.OUT_OF_RANGE

        if new_state != current_state:
            current_state = new_state
            print(new_state, s)

        time.sleep_ms(20)

def testThread():
    while True:
        print("Hello from thread")
        time.sleep(2)


# _thread.start_new_thread(testThread, ())

class RingBuffer:

    def __init__(self, size):
        self.size = size
        self.buffer = array('I')
        self.index = 0
        for i in range(0,5):
            self.buffer.append(0)

    def update(self, n):
        self.buffer[self.index] = n
        self.index += 1
        if self.index == self.size:
            self.index = 0

    def mean(self):
        return sum(rb.buffer)/self.size

    def std(self):
        mu = self.mean()

        def deviation_squared(n):
            return (mu-n)**2

        sum_of_squares = sum(map(deviation_squared, self.buffer))
        return math.sqrt(sum_of_squares / self.size)

    def z_scores(self):
        mu = self.mean()
        std = self.std()

        def z_score(n):
            return (n-mu)/std

        def zero(n: object):
            return 0

        if std == 0:
            return map(zero, self.buffer)

        return map(z_score, self.buffer)

    def is_stable(self):
        scores = list(self.z_scores())
        return max(scores) < 1.0 and min(scores) > -1.0


rb = RingBuffer(5)
