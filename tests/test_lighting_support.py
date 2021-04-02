import pytest
from lighting_support import LedPwmChannels
import ujson

@pytest.fixture
def pwm_channels():
    pwm_channels = LedPwmChannels(red_pin=1, green_pin=2, blue_pin=3, white_pin=4, uv_pin=5)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    return pwm_channels


def test_zero_duty(pwm_channels):
    pwm_channels.zero_duty()
    assert pwm_channels.red.current_duty == 0
    assert pwm_channels.green.current_duty == 0
    assert pwm_channels.blue.current_duty == 0
    assert pwm_channels.white.current_duty == 0
    assert pwm_channels.ultra_violet.current_duty == 0


def test_as_json(pwm_channels):
    expected_json = ujson.loads("""{"Red": 10, "Green": 20, "Blue": 30, "White": 40, "UltraViolet": 50}""")
    assert pwm_channels.as_json() == expected_json
