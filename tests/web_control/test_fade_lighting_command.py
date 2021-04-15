from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.testing_support import *
import pytest


def test_set_fade_request_is_accepted():

    commands = [{"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_fade_requires_a_color_parameter():
    commands = [{"command": "fade", "time": 1, "unit": "s"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "The fade command requires a color parameter", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_set_color_request_requires_a_valid_color():

    commands = [{"command": "fade", "time": 1, "unit": "s", "color": "this is not a color"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid color parameter. Found [this is not a color]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_sleep_requires_a_time_parameter():

    commands = [{"command": "fade", "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "The fade command requires a time parameter", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_number():
    commands = [{"command": "fade", "time": "this is not a number", "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [this is not a number]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_positive_number():
    commands = [{"command": "fade", "time": -0.1, "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [-0.1]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_not_be_zero():
    commands = [{"command": "fade", "time": 0, "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [0]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_fade_requires_a_unit_parameter():

    commands = [{"command": "fade", "time": 1, "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "The fade command requires a unit parameter", "line": 1}]""")
    assert json.loads(response.body) == expected_body


@pytest.mark.parametrize("test_name, unit_value", [
    ("milliseconds", "ms"),
    ("seconds", "s"),
    ("minutes", "m"),
])
def test_unit_parameter_must_be_milliseconds_seconds_or_minutes(test_name, unit_value):
    commands = [{"command": "fade", "time": 1, "unit": unit_value, "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == [{"command": "fade", "time": 1, "unit": unit_value, "color": "#ffff00"}]


def test_any_other_unit_parameter_fails():
    commands = [{"command": "fade", "time": 1, "unit": "X", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid unit parameter. Found [X]", "line": 1}]""")
    assert json.loads(response.body) == expected_body
