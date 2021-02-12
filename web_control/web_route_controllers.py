import ujson

valid_colors = ["White", "Red", "Green", "Blue", "UltraViolet"]
valid_flash_parameters = ["Delay"]


class LightingRequestHandler:

    @staticmethod
    def handle_flash(request: LightingRequest):
        is_valid, error_response = LightingRequestHandler.validate_flash_request(request)
        if not is_valid:
            return error_response
        response = ujson.loads("{}")
        response["Delay"] = request.body.get("Delay")
        # TODO: hues
        return LightingResponse("200 OK", request.path, response)


    @staticmethod
    def validate_flash_request(request: LightingRequest):
        if request.protocol != "PUT":
            msg = ujson.loads('{"Error": "Expecting PUT action", "Action": "%s"}' % request.protocol)
            return False, LightingResponse("405 Method Not Allowed", request.path, msg)

        for key in request.body.keys():
            if key not in valid_flash_parameters:
                msg = ujson.loads('{"Error": "Invalid Parameter %s"}' % key)
                return False, LightingResponse("400 Bad Request", request.path, msg)

        return True, None

    @staticmethod
    def validate_colors_request(request: LightingRequest):
        if request.protocol != "PUT":
            msg = ujson.loads('{"Error": "Expecting PUT action", "Action": "%s"}' % request.protocol)
            return False, LightingResponse("405 Method Not Allowed", request.path, msg)

        for key in request.body.keys():
            if key not in valid_colors:
                msg = ujson.loads('{"Error": "Invalid Color", "Color": "%s"}' % key)
                return False, LightingResponse("400 Bad Request", request.path, msg)
        return True, None
