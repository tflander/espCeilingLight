import ujson, re
from rgb_duties_converter import RgbDutiesConverter
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


class LightingScriptRequestHandler:

    # TODO: extract time parser for use in the animation calculator
    time_pattern = re.compile(r"([0-9]+)([a-z]+)")

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

        return LightingScriptRequestHandler.validate_time_parameter(parts[1], i)

    @staticmethod
    def validate_time_parameter(time_param, i):
        result = LightingScriptRequestHandler.time_pattern.match(time_param)

        if result is None:
            return {'error': 'Invalid time parameter. Found [%s]' % time_param, 'line': i}

        time_and_units = result.groups()
        time_val = float(time_and_units[0])
        time_units = time_and_units[1]

        if time_val <= 0 or time_units not in ["ms", "s", "m"]:
            return {'error': 'Invalid time parameter. Found [%s]' % time_param, 'line': i}

    @staticmethod
    def validate_fade_command(i, command):
        parts = command.split()
        if len(parts) != 4:
            return {'error': "Invalid syntax. Requires 'fade [time] to [color]'", 'line': i}

        validation = LightingScriptRequestHandler.validate_color_command(i, parts[3])
        if validation is None:
            validation = LightingScriptRequestHandler.validate_time_parameter(parts[1], i)
        return validation
