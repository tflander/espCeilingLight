export AMPY_PORT=/dev/cu.SLAB_USBtoUART
ampy ls

echo "updating boot.py..."
ampy put boot.py
echo "updating led_pwm_channels.py..."
ampy put led_pwm_channels.py
echo "updating main.py..."
ampy put main.py
echo "updating touch_button.py..."
ampy put touch_button.py
echo "updating config.py..."
ampy put config.py
echo "updating wifiConnector.py..."
ampy put wifiConnector.py
echo "updating rgb_duties_converter.py..."
ampy put rgb_duties_converter.py
echo "updating lighting_script_runner.py..."
ampy put lighting_script_runner.py
echo "updating animation_calculator.py..."
ampy put animation_calculator.py
echo "updating duties.py..."
ampy put duties.py
echo "updating presets.py..."
ampy put presets.py

echo "updating web_route_controllers.py..."
ampy rmdir web_control || echo "ignoring that folder web_control does not exist"
ampy mkdir web_control
ampy put web_control/web_route_controllers.py web_control/web_route_controllers.py
echo "updating lighting_request.py..."
ampy put web_control/lighting_request.py web_control/lighting_request.py
echo "updating lighting_response.py..."
ampy put web_control/lighting_response.py web_control/lighting_response.py
echo "updating lighting_script_request_handler.py..."
ampy put web_control/lighting_script_request_handler.py web_control/lighting_script_request_handler.py

ampy rmdir parsers || echo "ignoring that folder parsers does not exist"
ampy mkdir parsers
echo "updating time_parser.py..."
ampy put parsers/time_parser.py parsers/time_parser.py
echo "updating command_parser.py..."
ampy put parsers/command_parser.py parsers/command_parser.py
echo "updating command_runner.py..."
ampy put parsers/command_runner.py parsers/command_runner.py
echo "updating expression_parser.py..."
ampy put parsers/expression_parser.py parsers/expression_parser.py
echo "updating parser_constants.py..."
ampy put parsers/parser_constants.py parsers/parser_constants.py

echo "resetting..."
ampy reset
echo "done."
