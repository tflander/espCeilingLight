from touch_button import *
from led_pwm_channels import *

program_and_version = ("12v RGBW Lighting", "0.0.0")
touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
# Rev 1
# led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)

# Rev 2
led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=5, blue_pin=22, white_pin=23, uv_pin=19)
