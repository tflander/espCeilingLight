from lighting_script_runner import LightingScriptRunner
from lighting_support import LedPwmChannels
from rgb_duties_converter import Duties
import pytest
import time, asyncio

@pytest.mark.parametrize("test_name, rgb_string, expected_duties", [
    ("pure red", "#ff0000", Duties(red=1020)),
    ("pure green", "#00ff00", Duties(green=1020)),
    ("pure blue", "#0000ff", Duties(blue=1020)),
    ("pure white", "#ffffff", Duties(white=1020)),
    ("pure cyan", "#00ffff", Duties(green=1020, blue=1020)),
    ("pure magenta", "#ff00ff", Duties(red=1020, blue=1020)),
    ("pure yellow", "#ffff00", Duties(red=1020, green=1020)),
    ("dim red", "#660000", Duties(red=408)),
    ("dim green", "#006600", Duties(green=408)),
    ("dim blue", "#000066", Duties(blue=408)),
    ("dim white", "#666666", Duties(white=408)),
    ("bright red", "#ff6666", Duties(red=612, white=408)),
    ("bright green", "#66ff66", Duties(green=612, white=408)),
    ("bright blue", "#6666ff", Duties(blue=612, white=408)),
    ("bright cyan", "#66ffff", Duties(green=612, blue=612, white=408)),
    ("bright magenta", "#ff66ff", Duties(red=612, blue=612, white=408)),
    ("bright yellow", "#ffff66", Duties(red=612, green=612, white=408)),
])
def test_set_color(test_name, rgb_string, expected_duties):
    commands = [{"command": "setColor", "color": rgb_string}]
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    asyncio.run(LightingScriptRunner.run(commands, pwm_channels))
    assert pwm_channels.red.duty() == expected_duties.red
    assert pwm_channels.green.duty() == expected_duties.green
    assert pwm_channels.blue.duty() == expected_duties.blue
    assert pwm_channels.white.duty() == expected_duties.white
    assert pwm_channels.ultra_violet.duty() == expected_duties.ultra_violet


@pytest.mark.parametrize("test_name, delay_time, delay_units, expected_delay", [
    ("one second", 1, "s", 1.0),
    ("two seconds", 2, "s", 2.0),
    ("100 ms", 100, "ms", 0.1),
    ("2 seconds as a fraction of a minute", 0.03, "m", 2.0),
])
def test_sleep(test_name, delay_time, delay_units, expected_delay):
    commands = [{"command": "sleep", "time": delay_time, "unit": delay_units}]
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    start = time.time()
    asyncio.run(LightingScriptRunner.run(commands, pwm_channels))
    elapsed = time.time() - start
    assert elapsed == pytest.approx(expected_delay, 0.1)
