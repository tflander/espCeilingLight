import ujson


class LightingRequest:

    def __init__(self, raw_request: str):
        request = str(raw_request).split("\\r\\n")
        request_protocol_and_path = request[0].split()
        if len(request_protocol_and_path) < 2:
            self.body = None
        self.path = request_protocol_and_path[1]
        self.protocol = request_protocol_and_path[0][2:]
        self.raw_json = request[len(request) - 1]
        stripped = self.raw_json.replace("\\n", " ").replace("\\t", " ").replace("'", "")
        try:
            self.body = ujson.loads(stripped)
        except ValueError:
            self.body = None
