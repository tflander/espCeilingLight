import ujson
from web_control.lighting_request import LightingRequest
from web_control.lighting_response import LightingResponse


class LightingCommandsRequestHandler:
    @staticmethod
    def handle_lighting(request: LightingRequest):

        # TODO: validate commands
        # is_valid, error_response = LightingRequestHandler.validate_colors_request(request)
        # if not is_valid:
        #     return error_response

        return LightingResponse("200 OK", request.path, request.body)
