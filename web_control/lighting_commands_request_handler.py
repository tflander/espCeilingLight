import ujson
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


class LightingCommandsRequestHandler:
    @staticmethod
    def handle_lighting(request: LightingRequest):

        if request.body is None or len(request.body) == 0:
            msg = "invalid request body [%s]" % request.raw_json
            return LightingResponse("400 Bad Request", request.path, """{"error": "%s"}""" % msg)

        errors = []
        for i, command in enumerate(request.body, start=1):

            error = LightingCommandsRequestHandler.validate_command(i, command)
            if error is not None:
                errors.append(error)

        if len(errors) > 0:
            return LightingResponse("400 Bad Request", request.path, ujson.dumps(errors))

        return LightingResponse("200 OK", request.path, request.body)

    @staticmethod
    def validate_command(i, command):
        if 'color' not in command:
            return {'error': 'The setColor command requires a color parameter', 'line': i}

        if not LightingCommandsRequestHandler.is_valid_color(command['color']):
            return {'error': 'Invalid color parameter. Found [%s]' % command['color'], 'line': i}
        return None

    @staticmethod
    def is_valid_color(color: str):
        return color.startswith('#')
