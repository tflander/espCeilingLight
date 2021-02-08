import machine
import math, utime
import ujson

from touch_button import *
from lighting_modes import *
from party import *
from web_route_controllers import *

from ntptime import settime
import uasyncio
import usocket

settime()

print("opening listener on port 80")
s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)
print("listener opened")

last_web_command = None


async def web_command_listener(event: uasyncio.Event):

    global last_web_command

    request_handler = LightingRequestHandler()

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
        raw_request = conn.recv(1024)
        print('Content = %s' % raw_request)

        lighting_request = LightingRequest(raw_request)
        code, lighting_response = request_handler.handle(lighting_request)

        last_web_command = lighting_request
        event.set()

        conn.send('HTTP/1.1 %s OK\n' % code)
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(lighting_response)
        conn.close()

touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))

mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

# Rev 1
led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)

# Rev 2
# led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=5, blue_pin=22, white_pin=23, uv_pin=19)

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
    lighting_modes = LightModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    # button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    lighting_modes.activate()
    global last_selected_button, last_web_command
    event = uasyncio.Event()
    uasyncio.create_task(activate_button_listener(event))
    uasyncio.create_task(web_command_listener(event))

    while True:

        # TODO: wait for either web request or button select
        if event.is_set():
            # selected_button = button_collection.get_selected_button()
            print("triggered", last_selected_button, last_web_command)

            if last_selected_button >= 0:
                lighting_modes.deactivate()
            if last_selected_button == 0:
                lighting_modes.next_mode()
            elif last_selected_button == 1:
                lighting_modes.next_hue()
            elif last_selected_button == 2:
                lighting_modes.next_brightness_or_speed()
            elif last_web_command is not None:
                print("triggered", last_selected_button, last_web_command)
            lighting_modes.activate()
            event.clear()
            last_selected_button = -1
            last_web_command = None
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
