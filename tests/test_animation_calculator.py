from led_pwm_channels import LedPwmChannels
from animation_calculator import AnimationCalculator
from duties import Duties
import pytest


@pytest.fixture
def pwm_channels():
    pwm_channels = LedPwmChannels(red_pin=1, green_pin=2, blue_pin=3, white_pin=4, uv_pin=5)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    return pwm_channels


def test_fade_time_slice_defaults_to_10ms(pwm_channels):
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}

    fade_params = AnimationCalculator.for_fade_command(fade_command, pwm_channels)
    assert fade_params.slice_duration_ms == 10


def test_can_override_default_fade_time_slice(pwm_channels):
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}

    fade_params = AnimationCalculator.for_fade_command(fade_command, pwm_channels, slice_duration_ms=20)
    assert fade_params.slice_duration_ms == 20


def test_fade_target_color(pwm_channels):
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffcc00"}

    fade_params = AnimationCalculator.for_fade_command(fade_command, pwm_channels)
    assert fade_params.target_color == Duties(red=1020, green=816)


def test_fade_color_slice_deltas(pwm_channels):
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffcc00"}

    fade_params = AnimationCalculator.for_fade_command(fade_command, pwm_channels, slice_duration_ms=10)
    assert fade_params.color_slice_deltas == Duties(red=10.1, green=7.96, blue=-0.3, white=-0.4, ultra_violet=-0.5)
