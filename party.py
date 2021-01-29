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


class OneColorGlow:

    def __init__(self):
        self.color_channel = led_pwm_channels.green

    async def activate(self):
        while True:
            for i in range(0, 1023, 5):
                self.color_channel.duty(i)
                await uasyncio.sleep_ms(10)
            for i in range(1023, 0, -5):
                self.color_channel.duty(i)
                await uasyncio.sleep_ms(10)


class TwoColorFlash:

    def __init__(self):
        self.color_channel1 = led_pwm_channels.red
        self.color_channel2 = led_pwm_channels.blue

    async def activate(self):
        while True:
            self.color_channel1.duty(1023)
            self.color_channel2.duty(0)
            await uasyncio.sleep_ms(300)
            self.color_channel1.duty(0)
            self.color_channel2.duty(1023)
            await uasyncio.sleep_ms(300)


class PartyModes:

    modes = (TwoColorFlash(), OneColorGlow())

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None
        self.current_mode_index = 0

    def current_mode(self):
        return PartyModes.modes[self.current_mode_index]

    def activate(self):
        self.task = uasyncio.create_task(self.current_mode().activate())

    def next_mode(self):
        if self.current_mode_index == 0:
            self.current_mode_index = 1
        else:
            self.current_mode_index = 0

    def next_adjustment(self):
        pass

    # TODO: generic deactivate in super-class
    def deactivate(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None
        led_pwm_channels.zero_duty()


