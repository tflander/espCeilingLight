import pytest
from touch_button import AdjustParameters, TouchButton, TouchState
import machine


@pytest.fixture
def touch_button():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    return TouchButton(machine.Pin(4), touch_adjust_parameters)


def test_touch_button_default_state_is_unknown(touch_button):
    assert touch_button.state == TouchState.UNKNOWN


def test_touch_button_set_state_to_selected(touch_button):
    touch_button.touch.expect_next_read_value(125)

    assert touch_button.is_state_changed()
    assert touch_button.state == TouchState.SELECTED


def test_touch_button_set_state_to_released(touch_button):
    touch_button.touch.expect_next_read_value(400)

    assert touch_button.is_state_changed()
    assert touch_button.state == TouchState.RELEASED
