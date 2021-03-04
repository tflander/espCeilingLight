import machine


class LedPwmChannels:

    def __init__(self, red_pin, green_pin, blue_pin, white_pin, uv_pin):
        self.red = machine.PWM(machine.Pin(red_pin), freq=70, duty=0)
        self.green = machine.PWM(machine.Pin(green_pin), freq=70, duty=0)
        self.blue = machine.PWM(machine.Pin(blue_pin), freq=70, duty=0)
        self.white = machine.PWM(machine.Pin(white_pin), freq=70, duty=0)
        self.ultra_violet = machine.PWM(machine.Pin(uv_pin), freq=70, duty=0)

    def zero_duty(self):
        self.red.duty(0)
        self.green.duty(0)
        self.blue.duty(0)
        self.white.duty(0)
        self.ultra_violet.duty(0)

    def show_hue(self, hue, duty):
        self.red.duty(duty * hue[0])
        self.green.duty(duty * hue[1])
        self.blue.duty(duty * hue[2])

    def show_color(self, color):
        self.red.duty(color[0])
        self.green.duty(color[1])
        self.blue.duty(color[2])


class AvailableIntensities:

    FULL = 1023
    HALF = 512
    QUARTER = 256
    EIGHTH = 128


class RgbColors:
    RED = (1, 0, 0)
    YELLOW = (1, 1, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    CYAN = (0, 1, 1)
    MAGENTA = (1, 0, 1)
    BLACK = (0, 0, 0)
