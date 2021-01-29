# TODO: move abstract stuff to a different library
from lighting_modes import *
import uasyncio
from touch_button import *

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)
touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)


async def two_color_flash():
    while True:
        led_pwm_channels.red.duty(1023)
        led_pwm_channels.blue.duty(0)
        await uasyncio.sleep_ms(300)
        led_pwm_channels.red.duty(0)
        led_pwm_channels.blue.duty(1023)
        await uasyncio.sleep_ms(300)


async def color_glow():
    while True:
        for i in range(0, 1023, 5):
            led_pwm_channels.green.duty(i)
            await uasyncio.sleep_ms(10)
        for i in range(1023, 0, -5):
            led_pwm_channels.green.duty(i)
            await uasyncio.sleep_ms(10)


def control_animation():
    party_modes = PartyModes(led_pwm_channels)
    led_pwm_channels.zero_duty()
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    party_modes.activate()

    while True:

        selected_button = await button_collection.wait_for_button_select()

        party_modes.deactivate()
        if selected_button == 0:
            party_modes.next_mode()
        elif selected_button == 1:
            print("hue adjust not supported")
        else:
            print("brightness / speed not supported")
        party_modes.activate()
        uasyncio.sleep_ms(10)


def doit():
    uasyncio.run(control_animation())


class PartyModes:

    modes = (0, 1)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None
        self.current_mode_index = 0

    def activate(self):
        if self.current_mode_index == 0:
            self.task = uasyncio.create_task(two_color_flash())
        else:
            self.task = uasyncio.create_task(color_glow())

    def next_mode(self):
        if self.current_mode_index == 0:
            self.current_mode_index = 1
        else:
            self.current_mode_index = 0

    def next_adjustment(self):
        pass

    # TODO: generic deactivate in super-class
    def deactivate(self):
        print("party deactivate")
        if self.task is not None:
            self.task.cancel()
            self.task = None
        led_pwm_channels.zero_duty()


