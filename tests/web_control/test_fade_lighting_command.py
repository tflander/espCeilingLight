from web_control.lighting_commands_request_handler import LightingCommandsRequestHandler
from web_control.testing_support import *


def test_set_fade_request_is_accepted():

    commands = [{"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}]
    response = LightingCommandsRequestHandler.handle_lighting(create_request(commands))

    assert response.path == "/lighting"
    assert response.code == "200 OK"
    assert response.body == commands

# TODO: test validation for all fade parameters (re-use code)