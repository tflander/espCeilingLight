import machine
import math, utime
import ujson
from config import *
from lighting_script_runner import LightingScriptRunner
from presets import Presets

from touch_button import *
from lighting_modes import *
from party import *
from web_control.web_route_controllers import *

from ntptime import settime
import uasyncio
import json

settime()

last_web_command = None
web_listener_socket = start_listener()
current_task = None


async def web_command_listener(event: uasyncio.Event):

    global last_web_command

    while True:
        gc.collect()

        conn = None

        while conn is None:
            try:
                conn, addr = web_listener_socket.accept()
            except OSError as e:
                if e.args[0] == 11:
                    await uasyncio.sleep_ms(10)

        print('Got a connection from %s' % str(addr))
        raw_request = conn.recv(4096)
        print('Content = %s' % raw_request)

        lighting_request = LightingRequest(raw_request)
        lighting_response = LightingRequestHandler.handle(lighting_request)

        last_web_command = lighting_response
        event.set()

        conn.send('HTTP/1.1 %s\n' % lighting_response.code)
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(json.dumps(lighting_response.body))
        conn.close()


mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)

last_selected_button = -1


async def activate_button_listener(event: uasyncio.Event):
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    global last_selected_button
    while True:
        last_selected_button = await button_collection.wait_for_button_select()
        event.set()


async def handle_web_command(web_command):

    global current_task

    if web_command.path == '/colors':
        led_pwm_channels.zero_duty()
        led_pwm_channels.white.duty(web_command.body["White"])
        led_pwm_channels.red.duty(web_command.body["Red"])
        led_pwm_channels.green.duty(web_command.body["Green"])
        led_pwm_channels.blue.duty(web_command.body["Blue"])
        led_pwm_channels.ultra_violet.duty(web_command.body["UltraViolet"])
    elif web_command.path == '/lighting':
        if current_task is not None:
            current_task.cancel()
        current_task = uasyncio.create_task(LightingScriptRunner.run(web_command.body, led_pwm_channels))
    else:
        print("unknown web command [%s]" % web_command.path)


# TODO: dead code cleanup.
def perform_legacy_button_handling(lighting_modes):
    global last_selected_button
    lighting_modes.deactivate()

    print("last_selected_button", last_selected_button)
    if last_selected_button == 0:
        lighting_modes.next_mode()
    elif last_selected_button == 1:
        lighting_modes.next_hue()
    elif last_selected_button == 2:
        lighting_modes.next_brightness_or_speed()
    lighting_modes.activate()


def control_lighting():
    global last_selected_button, last_web_command

    lighting_modes = LightModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    lighting_modes.activate()

    event = uasyncio.Event()
    uasyncio.create_task(activate_button_listener(event))
    uasyncio.create_task(web_command_listener(event))

    while True:

        if event.is_set():

            global current_task

            if last_selected_button >= 0:
                # TODO: finish this
                # TODO: dead code cleanup.
                # perform_legacy_button_handling(lighting_modes)
                if current_task is not None:
                    current_task.cancel()
                    current_task = None
                # TODO: make this real
                presets = Presets(led_pwm_channels)
                preset = [{"command": "setColor", "color": "#ff0000"}]
                presets.add(preset)

                await presets.next()

            elif last_web_command is not None:
                if last_web_command.code == "200 OK":
                    if last_web_command.path != '/info':
                        lighting_modes.deactivate()
                    print("web command:", last_web_command.path, last_web_command.body)
                    await handle_web_command(last_web_command)
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
