from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.lighting_script_request_handler import LightingScriptRequestHandler
from web_control.testing_support import *


def test_legacy_set_color_request_is_accepted():

    commands = [{"color": "#ff0000", "command": "setColor"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_set_color_request_is_accepted():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["#ff0000"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_legacy_set_color_request_requires_a_color():

    commands = [{"command": "setColor"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "The setColor command requires a color parameter", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_legacy_set_color_request_requires_a_valid_color():

    commands = [{"command": "setColor", "color": "this is not a color"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid color parameter. Found [this is not a color]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_set_color_request_requires_a_valid_color():

    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["#this is not a color"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid color parameter. Found [#this is not a color]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


