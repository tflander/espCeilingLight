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
echo "updating wifiConnector.py..."
ampy put wifiConnector.py

# echo "updating web_route_controllers.py..."
# ampy put web_route_controllers.py

echo "creating web_control folder"
ampy mkdir web_control --exists-okay

echo "updating web_control/web_router.py"
ampy put web_control/web_router.py web_control/web_router.py

echo "updating web_control/color_controller.py"
ampy put web_control/color_controller.py web_control/color_controller.py

echo "updating web_control/flash_controller.py"
ampy put web_control/flash_controller.py web_control/flash_controller.py

echo "resetting..."
ampy reset
echo "done."
