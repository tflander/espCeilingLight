import ujson, re
from rgb_duties_converter import RgbDutiesConverter
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


class LightingScriptRequestHandler:
    @staticmethod
    def handle_lighting(request: LightingRequest):

        request_body = LightingScriptRequestHandler.create_response_body(request)
        if request_body is None or len(request_body) == 0:
            msg = "invalid request body [%s]" % request.raw_json
            return LightingResponse("400 Bad Request", request.path, """{"error": "%s"}""" % msg)

        errors = []
        # for i, command in enumerate(request.body, start=1):
        #
        #     error = LightingCommandsRequestHandler.validate_command(i, command)
        #     if error is not None:
        #         errors.append(error)
        #
        if len(errors) > 0:
            return LightingResponse("400 Bad Request", request.path, ujson.dumps(errors))

        return LightingResponse("200 OK", request.path, request_body)

    @staticmethod
    def create_response_body(request):

        # TODO: regex magic on ws in script (script element type from json string to json string array)
        regex = re.compile(r"^.*interfaceOpDataFile.*$", re.IGNORECASE)
        response_body = regex.sub("][", request.raw_json)

        response_body = request.raw_json
        return response_body
    # @staticmethod
    # def validate_command(i, command):
    #     if command['command'] == 'setColor':
    #         return LightingCommandsRequestHandler.validate_color_command(i, command)
    #     elif command['command'] == 'sleep':
    #         return LightingCommandsRequestHandler.validate_sleep_command(i, command)
    #     elif command['command'] == 'fade':
    #         return LightingCommandsRequestHandler.validate_fade_command(i, command)
    #     else:
    #         return {'error': 'Invalid command [%s]' % command['command'], 'line': i}
    #
    # @staticmethod
    # def validate_color_command(i, command):
    #     if 'color' not in command:
    #         return {'error': 'The %s command requires a color parameter' % command['command'], 'line': i}
    #
    #     if not RgbDutiesConverter.is_valid_color(command['color']):
    #         return {'error': 'Invalid color parameter. Found [%s]' % command['color'], 'line': i}
    #     return None
    #
    # @staticmethod
    # def validate_sleep_command(i, command):
    #     if 'time' not in command:
    #         return {'error': 'The %s command requires a time parameter' % command['command'], 'line': i}
    #
    #     if type(command['time']) != int and type(command['time']) != float:
    #         return {'error': 'Invalid time parameter. Found [%s]' % command['time'], 'line': i}
    #
    #     if command['time'] <= 0:
    #         return {'error': 'Invalid time parameter. Found [%s]' % command['time'], 'line': i}
    #
    #     if 'unit' not in command:
    #         return {'error': 'The %s command requires a unit parameter' % command['command'], 'line': i}
    #
    #     if command['unit'] not in ["ms", "s", "m"]:
    #         return {'error': 'Invalid unit parameter. Found [%s]' % command['unit'], 'line': i}
    #
    #     return None
    #
    # @staticmethod
    # def validate_fade_command(i, command):
    #     validation = LightingCommandsRequestHandler.validate_color_command(i, command)
    #     if validation is None:
    #         validation = LightingCommandsRequestHandler.validate_sleep_command(i, command)
    #     return validation
