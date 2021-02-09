import ujson


valid_colors = ["White", "Red", "Green", "Blue", "UltraViolet"]

class LightingRequest:

    def __init__(self, raw_request: str):
        request = str(raw_request).split("\\r\\n")
        request_protocol_and_path = request[0].split()
        self.path = request_protocol_and_path[1]
        self.protocol = request_protocol_and_path[0][2:]
        raw_json = request[len(request) - 1]
        stripped = raw_json.replace("\\n", " ").replace("\\t", " ").replace("'", "")
        try:
            self.body = ujson.loads(stripped)
        except ValueError:
            self.body = None


class LightingResponse:
    def __init__(self, code, path, body):
        self.code = code
        self.path = path
        self.body = body


class LightingRequestHandler:

    @staticmethod
    def handle(request: LightingRequest):
        if request.path == '/colors':
            return LightingRequestHandler.handle_colors(request)
        else:
            return LightingResponse("404 Not Found", request.path, ujson.loads('{"Error": "Unexpected path"}'))

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
            print(request.protocol)
            msg = ujson.loads('{"Error": "Expecting PUT action", "Action": "%s"}' % request.protocol)
            return False, LightingResponse("405 Method Not Allowed", request.path, msg)

        for key in request.body.keys():
            if key not in valid_colors:
                msg = ujson.loads('{"Error": "Invalid Color", "Color": "%s"}' % key)
                return False, LightingResponse("400 Bad Request", request.path, msg)
        return True, None
