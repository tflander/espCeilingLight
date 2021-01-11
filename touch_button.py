import utime
from machine import Pin, TouchPad

class TouchState:
    UNKNOWN = 1
    RELEASED = 2
    SELECTED = 3
    DEAD_BAND = 4
    OUT_OF_RANGE = 5


class AdjustParameters:

    def __init__(self, max_released, min_released, max_selected, min_selected):
        self.max_released = max_released
        self.min_released = min_released
        self.max_selected = max_selected
        self.min_selected = min_selected


class TouchButton:

    def __init__(self, touch_pin: Pin, adjust_parameters: AdjustParameters):
        self.touch = TouchPad(touch_pin)
        self.adjust_parameters = adjust_parameters

    def wait_for_state_change(self, current_state):
        while True:
            s = self.touch.read()
            if self.adjust_parameters.min_released < s < self.adjust_parameters.max_released:
                new_state = TouchState.RELEASED
            elif self.adjust_parameters.min_selected < s < self.adjust_parameters.max_selected:
                new_state = TouchState.SELECTED
            elif s < self.adjust_parameters.min_selected or s > self.adjust_parameters.max_released:
                new_state = TouchState.OUT_OF_RANGE
            else:
                new_state = TouchState.DEAD_BAND

            if new_state != current_state:
                return new_state
            utime.sleep_ms(20)
