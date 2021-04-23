import ujson, usocket
import ubinascii
import network
from config import *
from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse

valid_colors = ["White", "Red", "Green", "Blue", "UltraViolet"]


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
    def handle(request: LightingRequest):
        if request.path == '/colors':
            return LightingRequestHandler.handle_colors(request)
        elif request.path == '/lighting':
            return LightingCommandsRequestHandler.handle_lighting(request)
        elif request.path == '/info':
            return LightingRequestHandler.handle_info(request)
        else:
            return LightingResponse("404 Not Found", request.path, ujson.loads('{"Error": "Unexpected path [%s]"}' % request.path))

    @staticmethod
    def handle_info(request: LightingRequest):
        response = ujson.loads("{}")
        response["MacAddress"] = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        response["IP"] = network.WLAN().ifconfig()[0]
        response["Program"] = program_and_version[0]
        response["ProgramVersion"] = program_and_version[1]
        response["duties"] = led_pwm_channels.as_json()
        return LightingResponse("200 OK", request.path, response)

    @staticmethod
    def handle_colors(request: LightingRequest):

        is_valid, error_response = LightingRequestHandler.validate_colors_request(request)
        if not is_valid:
            return error_response

        response = ujson.loads("{}")
        response["White"] = request.body.get("White", 0)
        response["Red"] = request.body.get("Red", 0)
        response["Green"] = request.body.get("Green", 0)
        response["Blue"] = request.body.get("Blue", 0)
        response["UltraViolet"] = request.body.get("UltraViolet", 0)
        return LightingResponse("200 OK", request.path, response)

    @staticmethod
    def validate_colors_request(request: LightingRequest):
        if request.protocol != "PUT":
            msg = ujson.loads('{"Error": "Expecting PUT action", "Action": "%s"}' % request.protocol)
            return False, LightingResponse("405 Method Not Allowed", request.path, msg)

        if request.body is None:
            return False, LightingResponse("400 Bad Request", request.path, "invalid request body [%s]" % request.raw_json)

        for key in request.body.keys():
            if key not in valid_colors:
                msg = ujson.loads('{"Error": "Invalid Color", "Color": "%s"}' % key)
                return False, LightingResponse("400 Bad Request", request.path, msg)
        return True, None
