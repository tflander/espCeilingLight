class Pin:

    def __init__(self, pin):
        pass


class TouchPad:

    def __init__(self, pin):
        self.nextReadValue = 0;

    def expect_next_read_value(self, readValue):
        self.nextReadValue = readValue

    def read(self):
        return self.nextReadValue


class PWM:
    def __init__(self, pin, freq, duty):
        self.current_duty = duty
        self.duty_history = []

    def duty(self, value=None):
        if value is None:
            return self.current_duty
        else:
            self.current_duty = value
            self.duty_history.append(value)

    def reset_duty_history(self):
        self.duty_history = []
