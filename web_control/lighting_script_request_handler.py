import ujson, re
from rgb_duties_converter import RgbDutiesConverter
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


class LightingScriptRequestHandler:
    @staticmethod
    def handle_lighting(request: LightingRequest):

        if request.body is None or len(request.body) == 0:
            msg = "invalid request body [%s]" % request.raw_json
            return LightingResponse("400 Bad Request", request.path, """{"error": "%s"}""" % msg)

        if 'id' not in request.body:
            return LightingResponse("400 Bad Request", request.path, """{"error": "request must have an id"}""")

        if 'description' not in request.body:
            return LightingResponse("400 Bad Request", request.path, """{"error": "request must have a description"}""")

        if 'script' not in request.body:
            return LightingResponse("400 Bad Request", request.path, """{"error": "request must have a script"}""")

        script = request.body['script']

        if type(script) != list:
            return LightingResponse("400 Bad Request", request.path, """{"error": "script must be a string array"}""")

        if len(script) == 0:
            return LightingResponse("400 Bad Request", request.path, """{"error": "script must not be empty"}""")

        errors = []

        for i, command in enumerate(script, start=1):
            error = LightingScriptRequestHandler.validate_command(i, command)
            if error is not None:
                errors.append(error)

        if len(errors) > 0:
            return LightingResponse("400 Bad Request", request.path, ujson.dumps(errors))

        return LightingResponse("200 OK", request.path, request.body)

    @staticmethod
    def validate_command(i, command):
        pass
        if command.startswith("#"):
            return LightingScriptRequestHandler.validate_color_command(i, command)
        elif command.startswith('sleep'):
            return LightingScriptRequestHandler.validate_sleep_command(i, command)
        elif command.startswith('fade'):
            return LightingScriptRequestHandler.validate_fade_command(i, command)
    #     else:
    #         return {'error': 'Invalid command [%s]' % command['command'], 'line': i}

    @staticmethod
    def validate_color_command(i, command):
        if not RgbDutiesConverter.is_valid_color(command):
            return {'error': 'Invalid color parameter. Found [%s]' % command, 'line': i}
        return None

    @staticmethod
    def validate_sleep_command(i, command):
        parts = command.split()
        if len(parts) != 2:
            return {'error': "Invalid syntax. Requires 'sleep [time]'", 'line': i}
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
    @staticmethod
    def validate_fade_command(i, command):
        parts = command.split()
        if len(parts) != 4:
            return {'error': "Invalid syntax. Requires 'fade [time] to [color]'", 'line': i}

        validation = LightingScriptRequestHandler.validate_color_command(i, parts[3])
        return validation
        # if validation is None:
        #     validation = LightingCommandsRequestHandler.validate_sleep_command(i, command)
        # return validation
