import uasyncio
from lighting_script_runner import LightingScriptRunner
from led_pwm_channels import LedPwmChannels
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
def test_legacy_set_color(test_name, rgb_string, expected_duties):
    command = {"command": "setColor", "color": rgb_string}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    asyncio.run(LightingScriptRunner.run_legacy_command(command, pwm_channels))
    assert pwm_channels.red.duty() == expected_duties.red
    assert pwm_channels.green.duty() == expected_duties.green
    assert pwm_channels.blue.duty() == expected_duties.blue
    assert pwm_channels.white.duty() == expected_duties.white
    assert pwm_channels.ultra_violet.duty() == expected_duties.ultra_violet


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
    command = rgb_string
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
def test_legacy_sleep(test_name, delay_time, delay_units, expected_delay_ms):
    command = {"command": "sleep", "time": delay_time, "unit": delay_units}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_legacy_command(command, pwm_channels))
    assert uasyncio.total_sleep_time_ms == expected_delay_ms


@pytest.mark.parametrize("test_name, delay_value, expected_delay_ms", [
    ("one second", "1s", 1000),
    ("two seconds", "2s", 2000),
    ("100 ms", "100ms", 100),
    ("2 minutes", "2m", 120000),
])
def test_sleep(test_name, delay_value, expected_delay_ms):
    command = "sleep " + delay_value
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))
    assert uasyncio.total_sleep_time_ms == expected_delay_ms


def test_legacy_fade():
    command = {"command": "fade", "time": 1, "unit": "s", "color": "#ffff00"}
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_legacy_command(command, pwm_channels))
    assert uasyncio.total_sleep_time_ms == 1000
    assert pwm_channels.red.duty() == 1020
    assert pwm_channels.green.duty() == 1020
    assert pwm_channels.blue.duty() == 0
    assert pwm_channels.white.duty() == 0
    assert pwm_channels.ultra_violet.duty() == 0


def test_fade():
    command = "fade 1s to #ffff00"
    pwm_channels = LedPwmChannels(red_pin=2, green_pin=3, blue_pin=4, white_pin=5, uv_pin=6)
    pwm_channels.red.duty(10)
    pwm_channels.green.duty(20)
    pwm_channels.blue.duty(30)
    pwm_channels.white.duty(40)
    pwm_channels.ultra_violet.duty(50)
    uasyncio.total_sleep_time_ms = 0

    asyncio.run(LightingScriptRunner.run_command(command, pwm_channels))

    assert uasyncio.total_sleep_time_ms == 1000
    assert pwm_channels.red.duty_history == [
        10, 60, 111, 162, 212, 262, 313, 364, 414, 464, 515, 566, 616, 666, 717, 768, 818, 868, 919, 970, 1020
    ]
    assert pwm_channels.green.duty_history == [
        20, 70, 120, 170, 220, 270, 320, 370, 420, 470, 520, 570, 620, 670, 720, 770, 820, 870, 920, 970, 1020
    ]
    assert pwm_channels.blue.duty_history == [
        30, 28, 27, 26, 24, 22, 21, 20, 18, 16, 15, 14, 12, 10, 9, 8, 6, 4, 3, 2, 0
    ]
    assert pwm_channels.white.duty_history == [
        40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0
    ]
    assert pwm_channels.ultra_violet.duty_history == [
        50, 48, 45, 42, 40, 38, 35, 32, 30, 28, 25, 22, 20, 18, 15, 12, 10, 8, 5, 2, 0
    ]


# TODO: marker for new syntax support
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
