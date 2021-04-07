import json

from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.lighting_request import LightingRequest
from web_control.testing_support import *


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


def test_set_color_request_requires_a_valid_color():

    commands = [{"command": "setColor", "color": "this is not a color"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid color parameter. Found [this is not a color]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


