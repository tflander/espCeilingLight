from web_control.lighting_script_request_handler import LightingScriptRequestHandler
from web_control.testing_support import *
import pytest


def test_sleep_request_is_accepted():
    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep 2s"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


def test_sleep_requires_a_time_parameter():

    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid syntax. Requires 'sleep [time]'", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_number():
    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep xxx"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [xxx]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_be_a_positive_number():
    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep -0.1s"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [-0.1s]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_time_parameter_must_not_be_zero():
    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep 0s"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [0s]", "line": 1}]""")
    assert json.loads(response.body) == expected_body


def test_sleep_requires_a_unit_parameter():

    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep 10"]
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
        "description": "night-night",
        "script": ["sleep 10" + unit_value]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == {'description': 'night-night', 'id': 'foo', 'script': ['sleep 10' + unit_value]}


def test_any_other_unit_parameter_fails():
    commands = {
        "id": "foo",
        "description": "night-night",
        "script": ["sleep 10x"]
    }
    response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""[{"error": "Invalid time parameter. Found [10x]", "line": 1}]""")
    assert json.loads(response.body) == expected_body
