from lighting_support import LedPwmChannels
from animation_calculator import AnimationCalculator


def test_foo():
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)

    AnimationCalculator.for_fade_command(fade_command, pwm_channels)
