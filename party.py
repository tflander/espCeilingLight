# TODO: move abstract stuff to a different library
from lighting_modes import *
import uasyncio
from touch_button import *

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)
touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)


def control_animation():
    party_modes = LightModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    party_modes.activate()

    while True:

        selected_button = await button_collection.wait_for_button_select()

        party_modes.deactivate()
        if selected_button == 0:
            party_modes.next_mode()
        elif selected_button == 1:
            party_modes.next_hue()
        else:
            party_modes.next_brightness_or_speed()
        party_modes.activate()
        uasyncio.sleep_ms(10)


def doit():
    uasyncio.run(control_animation())


class OneColorGlow:

    def __init__(self, pwm_channels, hues):
        self.pwm_channels = pwm_channels
        self.hue_index = 0
        self.hues = hues

    async def activate(self):
        while True:
            for i in range(0, 1023, 5):
                self.pwm_channels.red.duty(i * self.hues[self.hue_index][0])
                self.pwm_channels.green.duty(i * self.hues[self.hue_index][1])
                self.pwm_channels.blue.duty(i * self.hues[self.hue_index][2])
                await uasyncio.sleep_ms(10)
            for i in range(1023, 0, -5):
                self.pwm_channels.red.duty(i * self.hues[self.hue_index][0])
                self.pwm_channels.green.duty(i * self.hues[self.hue_index][1])
                self.pwm_channels.blue.duty(i * self.hues[self.hue_index][2])
                await uasyncio.sleep_ms(10)

    def next_hue(self):
        self.hue_index += 1
        if self.hue_index == len(self.hues):
            self.hue_index = 0

    def next_brightness_or_speed(self):
        pass


class MultiColorFlash:

    delays = (100, 200, 300, 500, 800, 1300, 2100, 3400)

    def __init__(self, pwm_channels, hue_tuples):
        self.hue_tuples = hue_tuples
        self.current_hue_index = 0
        self.pwm_channels = pwm_channels
        self.delay_index = 0

    async def activate(self):
        hues = self.current_hue()  # e.g. (RgbColors.RED, RgbColors.BLUE)
        while True:
            for color_index_to_flash in range(0, len(hues)):
                self.pwm_channels.red.duty(1023 * hues[color_index_to_flash][0])
                self.pwm_channels.green.duty(1023 * hues[color_index_to_flash][1])
                self.pwm_channels.blue.duty(1023 * hues[color_index_to_flash][2])
                await uasyncio.sleep_ms(self.current_delay())

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


class LightModes:

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None
        self.current_mode_index = 0

        self.modes = (
            MultiColorFlash(self.pwm_channels, (
                (RgbColors.RED, RgbColors.BLUE),
                (RgbColors.BLUE, RgbColors.YELLOW),
                (RgbColors.RED, RgbColors.YELLOW, RgbColors.GREEN, RgbColors.CYAN, RgbColors.BLUE, RgbColors.MAGENTA)
            )),
            OneColorGlow(self.pwm_channels, (RgbColors.RED, RgbColors.GREEN, RgbColors.BLUE, RgbColors.CYAN, RgbColors.YELLOW, RgbColors.MAGENTA))
        )

    def current_mode(self):
        return self.modes[self.current_mode_index]

    def activate(self):
        self.task = uasyncio.create_task(self.current_mode().activate())

    def next_mode(self):
        if self.current_mode_index == 0:
            self.current_mode_index = 1
        else:
            self.current_mode_index = 0

    def next_hue(self):
        self.current_mode().next_hue()

    def next_brightness_or_speed(self):
        self.current_mode().next_brightness_or_speed()

    def deactivate(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None
        led_pwm_channels.zero_duty()


