from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.testing_support import *


def test_sleep_request_is_accepted():

    commands = [{"command": "sleep", "time": 1, "unit": "s"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == json.loads("""[{"command": "sleep", "time": 1, "unit": "s"}]""")
