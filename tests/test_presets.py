import asyncio

from lighting_support import LedPwmChannels
from presets import Presets


def test_add_preset():
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    presets = Presets(pwm_channels)

    preset = [{"command": "setColor", "color": "#ff0000"}]
    presets.add(preset)

    assert presets.presets[0] == preset


def test_next_preset():
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    presets = Presets(pwm_channels)
    preset = [{"command": "setColor", "color": "#ff0000"}]
    presets.add(preset)

    asyncio.run(presets.next())

    # asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))
    assert pwm_channels.red.duty() == 1020
    assert pwm_channels.green.duty() == 0
    assert pwm_channels.blue.duty() == 0
    assert pwm_channels.white.duty() == 0
    assert pwm_channels.ultra_violet.duty() == 0
