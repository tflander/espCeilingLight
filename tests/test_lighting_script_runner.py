import uasyncio
from lighting_script_runner import LightingScriptRunner
from lighting_support import LedPwmChannels
from duties import Duties
import pytest
import time, asyncio


# noinspection DuplicatedCode
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
    command = {"command": "setColor", "color": rgb_string}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))
    assert pwm_channels.red.duty() == expected_duties.red
    assert pwm_channels.green.duty() == expected_duties.green
    assert pwm_channels.blue.duty() == expected_duties.blue
    assert pwm_channels.white.duty() == expected_duties.white
    assert pwm_channels.ultra_violet.duty() == expected_duties.ultra_violet


@pytest.mark.parametrize("test_name, delay_time, delay_units, expected_delay_ms", [
    ("one second", 1, "s", 1000),
    ("two seconds", 2, "s", 2000),
    ("100 ms", 100, "ms", 100),
    ("2 minutes", 2, "m", 120000),
])
def test_sleep(test_name, delay_time, delay_units, expected_delay_ms):
    command = {"command": "sleep", "time": delay_time, "unit": delay_units}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))
    assert uasyncio.total_sleep_time_ms == expected_delay_ms


def test_fade():
    command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))
    assert uasyncio.total_sleep_time_ms == 1000
    assert pwm_channels.red.duty() == 1020
    assert pwm_channels.green.duty() == 1020
    assert pwm_channels.blue.duty() == 0
    assert pwm_channels.white.duty() == 0
    assert pwm_channels.ultra_violet.duty() == 0


def test_should_run_in_loop_for_commands_with_no_sleep_or_fade():
    commands = [{"command": "setColor", "color": "#ff0000"}]
    assert not LightingScriptRunner.should_run_in_loop(commands)


def test_should_run_in_loop_for_commands_containing_sleep():
    commands = [
        {"command": "setColor", "color": "#ff0000"},
        {"command": "sleep", "time": 1, "unit": "s"},
        {"command": "setColor", "color": "#ff0000"},
        {"command": "sleep", "time": 1, "unit": "s"}
    ]
    assert LightingScriptRunner.should_run_in_loop(commands)


def test_should_run_in_loop_for_commands_containing_fade():
    commands = [
        {"command": "fade", "color": "#ff0000", "time": 1, "unit": "s"},
        {"command": "fade", "color": "#00ff00", "time": 1, "unit": "s"},
    ]
    assert LightingScriptRunner.should_run_in_loop(commands)
