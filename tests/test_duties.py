from animation_calculator import AnimationCalculator
from duties import Duties
from lighting_support import LedPwmChannels
import pytest

from rgb_duties_converter import RgbDutiesConverter


@pytest.fixture
def pwm_channels():
    pwm_channels = LedPwmChannels(red_pin=1, green_pin=2, blue_pin=3, white_pin=4, uv_pin=5)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    return pwm_channels


@pytest.mark.parametrize("test_name, target_color, current_duties, expected_as_float, expected_updated_values", [
    (
            "all colors get adjusted", "#ffff00",
            Duties(red=10, green=20, blue=30, white=40, ultra_violet=50),
            Duties(red=20.1, green=30.0, blue=29.7, white=39.6, ultra_violet=49.5),
            Duties(red=20, green=30, blue=30, white=40, ultra_violet=50)
    ),
    (
            "target color already achieved", "#ffff00",
            Duties(red=1020, green=1020),
            Duties(red=1020, green=1020),
            Duties(red=1020, green=1020)
    ),
    (
            "last color cycle", "#ffff00",
            Duties(red=1019.999, green=1019.999, blue=0.001, white=0.001, ultra_violet=0.001),
            Duties(red=1020, green=1020),
            Duties(red=1020, green=1020)
    ),
])
def test_apply_deltas(pwm_channels, test_name, target_color, current_duties, expected_as_float, expected_updated_values):
    fade_command = {"command": "fade", "time": 1, "unit": "s", "color": target_color}
    fade_params = AnimationCalculator.for_fade_command(fade_command, pwm_channels)
    target_color_duties = RgbDutiesConverter.to_duties(target_color)
    duties_as_float = current_duties.apply_deltas(fade_params.color_slice_deltas, target_color_duties)

    assert duties_as_float == expected_as_float
    assert current_duties == expected_updated_values


