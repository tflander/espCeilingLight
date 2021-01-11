class TouchState:
    UNKNOWN = 1
    RELEASED = 2
    SELECTED = 3
    DEAD_BAND = 4
    OUT_OF_RANGE = 5


class AdustParameters:

    def __init__(self, max_released, min_released, max_selected, min_selected):
        self.max_released = max_released
        self.min_released = min_released
        self.max_selected = max_selected
        self.min_selected = min_selected

