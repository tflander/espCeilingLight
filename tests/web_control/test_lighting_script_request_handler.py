from web_control.lighting_script_request_handler import LightingScriptRequestHandler
from web_control.testing_support import *


def test_valid_request():
    commands = {
        "id": "foo",
        "description": "does cool stuff",
        "script": """
            #ff0000
            fade 2s to #0000ff
            sleep 2s
            fade 2s to #ff0000
        """
    }
    request = create_request(commands)
    response = LightingScriptRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands


# def test_request_must_have_an_id():
#     commands = {
#         "description": "does cool stuff",
#         "script": """
#             #ff0000
#             fade 2s to #0000ff
#             sleep 2s
#             fade 2s to #ff0000
#         """
#     }
#     response = LightingScriptRequestHandler.handle_lighting(create_request(commands))
#
#     assert response.path == "/lighting"
#     assert response.code == "400 Bad Request"
#     assert json.loads(response.body) == [
#         {"error": 'request must have an id'}
#     ]


# def test_invalid_command_is_rejected():
#
#     commands = [{"command": "invalid command"}]
#     response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
#
#     assert response.path == "/lighting"
#     assert response.code == "400 Bad Request"
#     assert json.loads(response.body) == [
#         {"error": 'Invalid command [invalid command]', 'line': 1}
#     ]
#
#
# def test_request_reports_lines_with_errors():
#
#     commands = [
#         {"command": "setColor", "color": "invalid color"},
#         {"command": "sleep", "time": 1, "unit": "invalid unit"},
#         {"command": "setColor", "color": "00ff00"},
#         {"command": "sleep", "time": 0, "unit": "s"}
#     ]
#     response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))
#
#     assert response.path == "/lighting"
#     assert response.code == "400 Bad Request"
#     assert json.loads(response.body) == [
#         {"error": 'Invalid color parameter. Found [invalid color]', 'line': 1},
#         {'error': 'Invalid unit parameter. Found [invalid unit]', 'line': 2},
#         {'error': 'Invalid color parameter. Found [00ff00]', 'line': 3},
#         {'error': 'Invalid time parameter. Found [0]', 'line': 4}
#     ]
#
#


def test_request_must_have_a_body():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b""))
    response = LightingScriptRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [ ']"}""")
    assert json.loads(response.body) == expected_body


def test_request_must_have_valid_json():

    request = LightingRequest(raw_request_template.replace(b"[commands]", b"this is not json"))
    response = LightingScriptRequestHandler.handle_lighting(request)

    assert response.path == "/lighting"
    assert response.code == "400 Bad Request"
    expected_body = json.loads("""{"error": "invalid request body [this is not json ']"}""")
    assert json.loads(response.body) == expected_body

