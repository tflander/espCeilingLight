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


class LightingRequestHandler:

    def handle(self, request: LightingRequest):
        if request.path == '/colors':
            pass

        return "200", "path = %s, body = %s" % (request.path, request.body)

