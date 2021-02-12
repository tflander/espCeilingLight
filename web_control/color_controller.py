from web_router import *


class ColorController:

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

