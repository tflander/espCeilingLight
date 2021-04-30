from web_control.lighting_script_request_handler import LightingScriptRequestHandler
from web_control.testing_support import *
import pytest


def test_set_fade_request_is_accepted():

    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 2s to #0000ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_fade_requires_four_parts():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 2s to"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid syntax. Requires 'fade [time] to [color]'", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_fade_request_requires_a_valid_color():

    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 2s to thisIsNotAColor"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid color parameter. Found [thisIsNotAColor]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_number():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade invalidTime to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [invalidTime]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_positive_number():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade -0.1s to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [-0.1s]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_not_be_zero():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 0s to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [0s]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_fade_requires_a_unit_parameter():

    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 10 to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [10]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


@pytest.mark.parametrize("test_name, unit_value", [
    ("milliseconds", "ms"),
    ("seconds", "s"),
    ("minutes", "m"),
])
def test_unit_parameter_must_be_milliseconds_seconds_or_minutes(test_name, unit_value):
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 10" + unit_value + " to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_any_other_unit_parameter_fails():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": ["fade 10x to #ff00ff"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [10x]", "line": 1}]""")
    assert json.loads(response.body) == expected_body
