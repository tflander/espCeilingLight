import gc
import uasyncio, ujson, usocket

from web_control.color_controller import *
from web_control.flash_controller import *

last_web_command = None


class LightingRequest:

    def __init__(self, raw_request: str):
        request = str(raw_request).split("\\r\\n")
        request_protocol_and_path = request[0].split()
        if len(request_protocol_and_path) < 2:
            self.body = None
        self.path = request_protocol_and_path[1]
        self.protocol = request_protocol_and_path[0][2:]
        raw_json = request[len(request) - 1]
        stripped = raw_json.replace("\\n", " ").replace("\\t", " ").replace("'", "")
        try:
            self.body = ujson.loads(stripped)
        except ValueError:
            self.body = None


class LightingResponse:
    def __init__(self, code, path, body):
        self.code = code
        self.path = path
        self.body = body


def handle(request: LightingRequest):
    if request.path == '/colors':
        return LightingRequestHandler.handle_colors(request)
    elif request.path == '/flash':
        return LightingRequestHandler.handle_flash(request)
    else:
        return LightingResponse("404 Not Found", request.path, ujson.loads('{"Error": "Unexpected path"}'))


async def web_command_listener(event: uasyncio.Event, s: usocket):

    global last_web_command

    while True:
        gc.collect()

        conn = None

        while conn is None:
            try:
                conn, addr = s.accept()
            except OSError as e:
                print("listener error", e)
                if e.args[0] == 11:
                    await uasyncio.sleep_ms(10)

        print('Got a connection from %s' % str(addr))
        raw_request = conn.recv(1024)
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
