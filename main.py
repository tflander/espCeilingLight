import machine
import math, utime
import ujson
from config import *
from lighting_script_runner import LightingScriptRunner
from presets import Presets

from touch_button import *

from web_control.web_route_controllers import *

import uasyncio
import json

last_web_command = None
web_listener_socket = start_listener()
current_task = None
current_script = None


async def web_command_listener(event: uasyncio.Event):

    global last_web_command, current_script

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

        lighting_response = LightingRequestHandler.handle(lighting_request, current_script)

        last_web_command = lighting_response
        event.set()

        conn.send('HTTP/1.1 %s\n' % lighting_response.code)
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(json.dumps(lighting_response.body))
        conn.close()

mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

last_selected_button = -1


async def activate_button_listener(event: uasyncio.Event):
    button_collection = TouchButtonCollection(mode_touch_button)
    global last_selected_button
    while True:
        last_selected_button = await button_collection.wait_for_button_select()
        event.set()


async def handle_web_command(web_command):

    global current_task, current_script

    if web_command.path == '/lighting':
        if current_task is not None:
            current_task.cancel()
        current_script = web_command.body['script']
        current_task = uasyncio.create_task(LightingScriptRunner.run(current_script, led_pwm_channels))
    else:
        print("unknown web command [%s]" % web_command.path)


presets = Presets()
presets.add(["#ff0000"])
presets.add(["#00ff00"])
presets.add(["#0000ff"])
presets.add(["#ccccff"])
presets.add([
    "#0000ff",
    "fade 2s to #ff0000",
    "fade 2s to #00ff00",
    "fade 2s to #0000ff"
])


def control_lighting():
    global last_selected_button, last_web_command, current_task, presets, current_script

    event = uasyncio.Event()
    uasyncio.create_task(activate_button_listener(event))
    uasyncio.create_task(web_command_listener(event))
    current_script = presets.next()
    current_task = uasyncio.create_task(LightingScriptRunner.run(current_script, led_pwm_channels))

    while True:

        if event.is_set():

            if last_selected_button >= 0:
                if current_task is not None:
                    current_task.cancel()
                    current_task = None
                current_script = presets.next()
                current_task = uasyncio.create_task(LightingScriptRunner.run(current_script, led_pwm_channels))

            elif last_web_command is not None:
                if last_web_command.code == "200 OK":
                    print("web command:", last_web_command.path, last_web_command.body)
                    await handle_web_command(last_web_command)
            event.clear()
            last_selected_button = -1
            last_web_command = None
        await uasyncio.sleep_ms(10)


print("running lights")
uasyncio.run(control_lighting())
