from web_control.web_route_controllers import LightingRequest, LightingResponse
import ujson


class LightingCommandsRequestHandler:
    @staticmethod
    def handle_lighting(request: LightingRequest):

        # is_valid, error_response = LightingRequestHandler.validate_colors_request(request)
        # if not is_valid:
        #     return error_response

        print(request.body)
        print(len(request.body))
        print(request.body[0])
        response = ujson.loads("{}")
        response["foo"] = "bar"
        return LightingResponse("200 OK", request.path, request.body)
