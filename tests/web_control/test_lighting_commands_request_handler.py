import json

from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.lighting_request import LightingRequest


def test_set_color_request_is_accepted():

    commands = [{"color": "#ff0000", "command": "setColor"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == json.loads("""[{"color": "#ff0000", "command": "setColor"}]""")


def test_request_must_have_a_body():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b""))
    response = LightingCommandsRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [ ']"}""")
    assert json.loads(response.body) == expected_body


def test_request_must_have_a_body():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b"this is not json"))
    response = LightingCommandsRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [this is not json ']"}""")
    assert json.loads(response.body) == expected_body


def test_set_color_request_requires_a_color():

    commands = [{"command": "setColor"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "The setColor command requires a color parameter", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def create_request(commands):
    raw_request = raw_request_template.replace(b"[commands]", json.dumps(commands).encode("utf-8"))
    return LightingRequest(raw_request)


raw_request_template = b"""PUT /lighting HTTP/1.1\r\nHost: 192.168.0.2\r\nConnection: keep-alive\r\nContent-Length: 
54\r\nPostman-Token: 0dcb8d52-e83a-3642-0228-f002a1600693\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (
Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 
Safari/537.36\r\nContent-Type: application/json\r\nAccept: */*\r\nOrigin: 
chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,
en;q=0.9\r\n\r\n[commands] """
