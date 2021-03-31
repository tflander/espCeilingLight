import pytest
from touch_button import AdjustParameters, TouchButton, TouchState
import machine


def test_touch_button_default_state_is_unknown():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
    assert mode_touch_button.state == TouchState.UNKNOWN
    # assert not mode_touch_button.is_state_changed()


def test_touch_button_set_state_to_selected():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

    mode_touch_button.touch.expect_next_read_value(125)

    assert mode_touch_button.is_state_changed()
    assert mode_touch_button.state == TouchState.SELECTED


def test_touch_button_set_state_to_released():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

    mode_touch_button.touch.expect_next_read_value(400)

    assert mode_touch_button.is_state_changed()
    assert mode_touch_button.state == TouchState.RELEASED
