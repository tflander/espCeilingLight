import asyncio
import pytest

from duties import Duties
from led_pwm_channels import LedPwmChannels
from presets import Presets


@pytest.fixture()
def presets():
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    presets = Presets(pwm_channels)

    preset1 = [{"command": "setColor", "color": "#ff0000"}]
    presets.add(preset1)
    preset2 = [{"command": "setColor", "color": "#00ff00"}]
    presets.add(preset2)
    preset3 = [{"command": "setColor", "color": "#0000ff"}]
    presets.add(preset3)
    return presets


def test_add_preset(presets):
    expected_presets = [
        [{"command": "setColor", "color": "#ff0000"}],
        [{"command": "setColor", "color": "#00ff00"}],
        [{"command": "setColor", "color": "#0000ff"}]
    ]
    assert presets.presets == expected_presets


def test_next_preset_cycles(presets):

    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(red=1020)
    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(green=1020)
    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(blue=1020)
    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(red=1020)
    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(green=1020)
    asyncio.run(presets.next())
    assert presets.pwm_channels.as_duties() == Duties(blue=1020)
