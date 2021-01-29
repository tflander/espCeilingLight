from machine import Pin, TouchPad
import uasyncio

class TouchState:
    UNKNOWN = 1
    RELEASED = 2
    SELECTED = 3
    DEAD_BAND = 4
    OUT_OF_RANGE = 5


class AdjustParameters:

    def __init__(self, limits: (int, int), dead_band: (int, int)):
        if limits[0] < limits[1]:
            self.max_released = limits[1]
            self.min_selected = limits[0]
        else:
            self.max_released = limits[0]
            self.min_selected = limits[1]

        if dead_band[0] < dead_band[1]:
            self.min_released = dead_band[1]
            self.max_selected = dead_band[0]
        else:
            self.min_released = dead_band[0]
            self.max_selected = dead_band[1]


class TouchButtonCollection:

    def __init__(self, *tuple_of_touch_buttons):
        for touch_button in tuple_of_touch_buttons:
            print(touch_button)
        self.button_tuple = tuple_of_touch_buttons

    async def wait_for_button_select(self):
        while True:
            for index, touch_button in enumerate(self.button_tuple):
                if touch_button.is_state_changed():
                    if touch_button.state == TouchState.SELECTED:
                        return index


class TouchButton:

    def __init__(self, touch_pin: Pin, adjust_parameters: AdjustParameters):
        self.touch = TouchPad(touch_pin)
        self.adjust_parameters = adjust_parameters
        self.state = TouchState.UNKNOWN

    def is_state_changed(self):
        s = self.touch.read()
        if self.adjust_parameters.min_released < s < self.adjust_parameters.max_released:
            new_state = TouchState.RELEASED
        elif self.adjust_parameters.min_selected < s < self.adjust_parameters.max_selected:
            new_state = TouchState.SELECTED
        elif s < self.adjust_parameters.min_selected or s > self.adjust_parameters.max_released:
            new_state = TouchState.OUT_OF_RANGE
        else:
            new_state = TouchState.DEAD_BAND

        if new_state != self.state:
            self.state = new_state
            return True
        return False

    async def wait_for_state_change(self):
        while not self.is_state_changed():
            await uasyncio.sleep_ms(20)

    async def wait_for_select(self):
        while True:
            await self.wait_for_state_change()
            if self.state == TouchState.SELECTED:
                return

    def show_read_values(self):
        while True:
            print(self.touch.read())
            uasyncio.sleep_ms(20)
