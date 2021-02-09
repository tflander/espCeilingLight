import ujson


class LightingRequest:

    def __init__(self, raw_request: str):
        request = str(raw_request).split("\\r\\n")
        request_protocol_and_path = request[0].split()
        self.path = request_protocol_and_path[1]

        if request_protocol_and_path[0].endswith("PUT"):
            self.protocol = "PUT"
        else:
            raise Exception("protocol %s not supported" % request_protocol_and_path[0])

        raw_json = request[len(request) - 1]
        stripped = raw_json.replace("\\n", " ").replace("\\t", " ").replace("'", "")
        self.body = ujson.loads(stripped)


class LightingResponse:
    def __init__(self, code, path, body):
        self.code = code
        self.path = path
        self.body = body


class LightingRequestHandler:

    @staticmethod
    def handle(request: LightingRequest):
        if request.path == '/colors':
            pass  # TODO: Validation, mapping, and all that sort of thing

        # TODO: instead of request.body, map to a new json
        return LightingResponse("200 OK", request.path, request.body)

