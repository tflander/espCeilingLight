import pytest
from touch_button import AdjustParameters, TouchButton
import machine


def test_is_state_changed():
    touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
    mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)

    assert False
