import machine
import math, utime

from touch_button import *
from lighting_modes import *
from party import *

from ntptime import settime
import uasyncio

settime()


import usocket

# Web server spike
print("opening listener on port 80")
s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)
print("listener opened")

last_web_command = ""


async def web_command_listener(event: uasyncio.Event):

    global last_web_command

    while True:
        gc.collect()

        conn = None

        while conn is None:
            try:
                conn, addr = s.accept()
            except OSError as e:
                if e.args[0] == 11:
                    await uasyncio.sleep_ms(10)

        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request).split("\\r\\n")
        request_protocol_and_path = request[0].split()
        print('Content = %s' % request)
        print('First Line = %s' % request[0].split())

        response = ""
        if request_protocol_and_path[0].endswith("GET"):
            response += "GET protocol<br />"
        else:
            response += "Unsupported protocol " + request_protocol_and_path[0]
        response += "Path = " + request_protocol_and_path[1]

        last_web_command = request_protocol_and_path[1]
        event.set()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))

mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)

last_selected_button = -1


async def activate_button_listener(event: uasyncio.Event):
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    global last_selected_button
    while True:
        last_selected_button = await button_collection.wait_for_button_select()
        event.set()


def event_spike():
    event = uasyncio.Event()
    global last_selected_button, last_web_command
    uasyncio.create_task(activate_button_listener(event))
    uasyncio.create_task(web_command_listener(event))

    while True:
        if event.is_set():
            print("triggered", last_selected_button, last_web_command)
            event.clear()
            last_selected_button = -1
            last_web_command = ""
        await uasyncio.sleep_ms(20)


def control_lighting():
    party_modes = LightModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    party_modes.activate()

    while True:

        # TODO: wait for either web request or button select
        selected_button = button_collection.get_selected_button()
        if selected_button >= 0:
            party_modes.deactivate()
            if selected_button == 0:
                party_modes.next_mode()
            elif selected_button == 1:
                party_modes.next_hue()
            else:
                party_modes.next_brightness_or_speed()
            party_modes.activate()
        await uasyncio.sleep_ms(10)


class LightModes:

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None
        self.current_mode_index = 0

        self.modes = (
            WhiteModes(self.pwm_channels),
            RgbModes(self.pwm_channels),
            MultiColorFlash(self.pwm_channels, (
                (RgbColors.RED, RgbColors.BLUE),
                (RgbColors.BLUE, RgbColors.YELLOW),
                (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.CYAN, RgbColors.BLUE, RgbColors.MAGENTA)
            )),
            OneColorGlow(self.pwm_channels, (
                RgbColors.RED,
                RgbColors.GREEN,
                RgbColors.BLUE,
                RgbColors.CYAN,
                RgbColors.YELLOW,
                RgbColors.MAGENTA)
            ),
            MultiColorFade(self.pwm_channels, (
                (RgbColors.RED, RgbColors.BLUE),
                (RgbColors.BLUE, RgbColors.GREEN),
                (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.CYAN, RgbColors.BLUE, RgbColors.MAGENTA)
            ))
        )

    def current_mode(self):
        return self.modes[self.current_mode_index]

    def activate(self):
        self.task = uasyncio.create_task(self.current_mode().activate())

    def next_mode(self):
        self.current_mode_index += 1
        if self.current_mode_index == len(self.modes):
            self.current_mode_index = 0

    def next_hue(self):
        self.current_mode().next_hue()

    def next_brightness_or_speed(self):
        self.current_mode().next_brightness_or_speed()

    def deactivate(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None
        led_pwm_channels.zero_duty()


print("running lights")
uasyncio.run(control_lighting())
# print("event spike")
# uasyncio.run(event_spike())
