from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.testing_support import *


def test_request_must_have_a_body():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b""))
    response = LightingCommandsRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [ ']"}""")
    assert json.loads(response.body) == expected_body


def test_request_must_have_valid_json():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b"this is not json"))
    response = LightingCommandsRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [this is not json ']"}""")
    assert json.loads(response.body) == expected_body

