import machine
import math, time, utime

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

def showTouch():
    while True:
        print(touch.read())
        time.sleep_ms(200)

