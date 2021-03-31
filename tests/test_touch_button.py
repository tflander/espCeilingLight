import asyncio

import pytest
from touch_button import AdjustParameters, TouchButton, TouchState
import machine


@pytest.fixture
def touch_button():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    return TouchButton(machine.Pin(4), touch_adjust_parameters)


def test_touch_button_default_state_is_unknown(touch_button):
    assert touch_button.state == TouchState.UNKNOWN


@pytest.mark.parametrize("touch_value, is_state_changed, expected_button_state", [
    (0, True, TouchState.OUT_OF_RANGE),
    (49, True, TouchState.OUT_OF_RANGE),
    (50, True, TouchState.SELECTED),
    (174, True, TouchState.SELECTED),
    (175, True, TouchState.DEAD_BAND),
    (250, True, TouchState.DEAD_BAND),
    (251, True, TouchState.RELEASED),
    (599, True, TouchState.RELEASED),
    (600, True, TouchState.OUT_OF_RANGE),
    (1024, True, TouchState.OUT_OF_RANGE),
])
def test_state_change_from_unknown(touch_button, touch_value, is_state_changed, expected_button_state):
    touch_button.touch.expect_next_read_value(touch_value)

    assert touch_button.is_state_changed() == is_state_changed
    assert touch_button.state == expected_button_state


@pytest.mark.asyncio
async def test_wait_for_button_release(touch_button):
    touch_button.touch.expect_next_read_value(400)
    await touch_button.wait_for_state_change()
    assert touch_button.state == TouchState.RELEASED


@pytest.mark.asyncio
async def test_wait_for_button_select(touch_button):
    touch_button.touch.expect_next_read_value(125)
    await touch_button.wait_for_state_change()
    assert touch_button.state == TouchState.SELECTED


