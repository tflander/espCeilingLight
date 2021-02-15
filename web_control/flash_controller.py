from web_control.web_router import *


class FlashController:

    @staticmethod
    def handle_flash(request: LightingRequest):

        is_valid, error_response = LightingRequestHandler.validate_flash_request(request)
        if not is_valid:
            return error_response
        response = ujson.loads("{}")
        response["Delay"] = request.body.get("Delay")
        # TODO: hues
        return LightingResponse("200 OK", request.path, response)

