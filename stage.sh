export AMPY_PORT=/dev/cu.SLAB_USBtoUART
ampy ls

echo "updating boot.py..."
ampy put boot.py
echo "updating lighting_modes.py..."
ampy put lighting_modes.py
echo "updating lighting_support.py..."
ampy put lighting_support.py
echo "updating main.py..."
ampy put main.py
echo "updating party.py..."
ampy put party.py
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

echo "updating web_route_controllers.py..."
ampy rmdir web_control || echo "ignoring that folder web_control does not exist"
ampy mkdir web_control
ampy put web_control/web_route_controllers.py web_control/web_route_controllers.py
echo "updating lighting_request.py..."
ampy put web_control/lighting_request.py web_control/lighting_request.py
echo "updating lighting_response.py..."
ampy put web_control/lighting_response.py web_control/lighting_response.py
echo "updating lighting_commands_request_handler.py..."
ampy put web_control/lighting_commands_request_handler.py web_control/lighting_commands_request_handler.py

echo "resetting..."
ampy reset
echo "done."
