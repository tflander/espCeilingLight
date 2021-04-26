import ujson, usocket
import ubinascii
import network
from config import *
from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


def start_listener():
    print("opening listener on port 80")
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False)
    print("listener opened")
    return s


class LightingRequestHandler:

    @staticmethod
    def handle(request: LightingRequest, script):
        if request.path == '/lighting':
            return LightingCommandsRequestHandler.handle_lighting(request)
        elif request.path == '/info':
            return LightingRequestHandler.handle_info(request, script)
        else:
            return LightingResponse("404 Not Found", request.path, ujson.loads('{"Error": "Unexpected path [%s]"}' % request.path))

    @staticmethod
    def handle_info(request: LightingRequest, script):
        response = ujson.loads("{}")
        response["MacAddress"] = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        response["IP"] = network.WLAN().ifconfig()[0]
        response["Program"] = program_and_version[0]
        response["ProgramVersion"] = program_and_version[1]
        response["duties"] = led_pwm_channels.as_json()
        response["script"] = script
        return LightingResponse("200 OK", request.path, response)
