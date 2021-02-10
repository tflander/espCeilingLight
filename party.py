import uasyncio


class OneColorGlow:

    def __init__(self, pwm_channels, hues):
        self.pwm_channels = pwm_channels
        self.hue_index = 0
        self.hues = hues
        self.fade_steps = (1, 2, 3, 5, 8, 13, 21)
        self.fade_steps_index = 0

    async def activate(self):
        while True:
            for i in range(0, 1023, self.fade_steps[self.fade_steps_index]):
                self.pwm_channels.show_hue(self.hues[self.hue_index], i)
                await uasyncio.sleep_ms(10)
            for i in range(1023, 0, -1 * self.fade_steps[self.fade_steps_index]):
                self.pwm_channels.show_hue(self.hues[self.hue_index], i)
                await uasyncio.sleep_ms(10)

    def next_hue(self):
        self.hue_index += 1
        if self.hue_index == len(self.hues):
            self.hue_index = 0

    def next_brightness_or_speed(self):
        self.fade_steps_index += 1
        if self.fade_steps_index == len(self.fade_steps):
            self.fade_steps_index = 0


class MultiColorFade:

    def __init__(self, pwm_channels, hue_tuples):
        self.pwm_channels = pwm_channels
        self.hue_tuples = hue_tuples
        self.current_hue_index = 0
        self.fade_steps = (1, 2, 3, 5, 8, 13, 21)
        self.fade_steps_index = 0

    async def activate(self):
        hues = self.current_hue()
        while True:
            for color_index_to_fade_from in range(0, len(hues)):
                current_color = list(map(lambda c: c * 1023, hues[color_index_to_fade_from]))
                self.pwm_channels.show_color(current_color)
                await uasyncio.sleep_ms(10)

                next_color_index = color_index_to_fade_from + 1
                if next_color_index == len(hues):
                    next_color_index = 0

                next_color = list(map(lambda c: c * 1023, hues[next_color_index]))

                steps_for_fading = self.fade_steps[self.fade_steps_index]
                while current_color != next_color:
                    for pixel in range(0, 3):
                        if current_color[pixel] < next_color[pixel]:
                            current_color[pixel] += steps_for_fading
                            if current_color[pixel] > next_color[pixel]:
                                current_color[pixel] = next_color[pixel]
                        elif current_color[pixel] > next_color[pixel]:
                            current_color[pixel] -= steps_for_fading
                            if current_color[pixel] < next_color[pixel]:
                                current_color[pixel] = next_color[pixel]
                    self.pwm_channels.show_color(current_color)
                    await uasyncio.sleep_ms(10)

    def next_hue(self):
        self.current_hue_index += 1
        if self.current_hue_index == len(self.hue_tuples):
            self.current_hue_index = 0

    def current_hue(self):
        return self.hue_tuples[self.current_hue_index]

    def next_brightness_or_speed(self):
        self.fade_steps_index += 1
        if self.fade_steps_index == len(self.fade_steps):
            self.fade_steps_index = 0


class MultiColorFlash:

    delays = (100, 200, 300, 500, 800, 1300, 2100, 3400)

    def __init__(self, pwm_channels, hue_tuples):
        self.hue_tuples = hue_tuples
        self.current_hue_index = 0
        self.pwm_channels = pwm_channels
        self.delay_index = 0

    async def activate(self):
        await MultiColorFlash.flash(self.pwm_channels, self.current_hue(), self.current_delay())

    @staticmethod
    async def flash(led_pwm_channels, hues, delay):
        while True:
            for color_index_to_flash in range(0, len(hues)):
                led_pwm_channels.show_hue(hues[color_index_to_flash], 1023)
                await uasyncio.sleep_ms(delay)

    def next_hue(self):
        self.current_hue_index += 1
        if self.current_hue_index == len(self.hue_tuples):
            self.current_hue_index = 0

    def next_brightness_or_speed(self):
        self.delay_index += 1
        if self.delay_index == len(MultiColorFlash.delays):
            self.delay_index = 0

    def current_hue(self):
        return self.hue_tuples[self.current_hue_index]

    def current_delay(self):
        return MultiColorFlash.delays[self.delay_index]



