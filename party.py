# TODO: move abstract stuff to a different library
from lighting_modes import *
import uasyncio
from touch_button import *

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)
touch_adjust_parameters = AdjustParameters(limits=(50, 600), dead_band=(175, 250))
mode_touch_button = TouchButton(machine.Pin(4), touch_adjust_parameters)
sub1_touch_button = TouchButton(machine.Pin(27), touch_adjust_parameters)
sub2_touch_button = TouchButton(machine.Pin(14), touch_adjust_parameters)


def button_collection_spike():
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    while True:
        print(await button_collection.wait_for_button_select())


async def first_party_animation():
    print("first animation")
    while True:
        led_pwm_channels.red.duty(1023)
        led_pwm_channels.blue.duty(0)
        await uasyncio.sleep_ms(300)
        led_pwm_channels.red.duty(0)
        led_pwm_channels.blue.duty(1023)
        await uasyncio.sleep_ms(300)


async def second_party_animation():
    print("second animation")
    while True:
        for i in range(0, 1023, 5):
            led_pwm_channels.green.duty(i)
            await uasyncio.sleep_ms(10)
        for i in range(1023, 0, -5):
            led_pwm_channels.green.duty(i)
            await uasyncio.sleep_ms(10)


def control_animation():
    animation_task = uasyncio.create_task(first_party_animation())
    button_collection = TouchButtonCollection(mode_touch_button, sub1_touch_button, sub2_touch_button)
    current_mode = 0
    while True:

        selected_button = await button_collection.wait_for_button_select()

        if selected_button == 0:
            print("mode change requested")
            animation_task.cancel()
            led_pwm_channels.zero_duty()
            if current_mode == 0:
                current_mode = 1
                animation_task = uasyncio.create_task(second_party_animation())
            else:
                current_mode = 0
                animation_task = uasyncio.create_task(first_party_animation())

        elif selected_button == 1:
            print("hue adjust not supported")
        else:
            print("brightness / speed not supported")
        uasyncio.sleep_ms(10)


def doit():
    uasyncio.run(control_animation())


class PartyModes:

    modes = (RgbColors.RED, RgbColors.BLUE, RgbColors.GREEN)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None

    def activate(self):
        # self.pwm_channels.red.duty(1023)  # stub for now
        print("party activate")
        # uasyncio.run(self.control_first_simple_animation())

        self.pwm_channels.red.duty(64 * self.current_mode()[0])
        self.pwm_channels.green.duty(64 * self.current_mode()[1])
        self.pwm_channels.blue.duty(64 * self.current_mode()[2])
        self.pwm_channels.red.freq(4)
        # this runs, but cannot be interrupted
        # uasyncio.run(control_animation())

    def next_adjustment(self):
        pass

    # TODO: generic deactivate in super-class
    def deactivate(self):
        print("party deactivate")
        # if self.task is not None:
        #    self.task.cancel()
        #    self.task = None
        self.pwm_channels.red.duty(0)
        self.pwm_channels.red.freq(60)
        self.pwm_channels.green.duty(0)
        self.pwm_channels.blue.duty(0)


class OldPartyModes(AbstractLightingMode):

    modes = (RgbColors.RED, RgbColors.BLUE, RgbColors.GREEN)

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.current_intensity_index = 0
        self.task = None

    def activate(self):
        # self.pwm_channels.red.duty(1023)  # stub for now
        print("party activate")
        # uasyncio.run(self.control_first_simple_animation())

        self.pwm_channels.red.duty(64 * self.current_mode()[0])
        self.pwm_channels.green.duty(64 * self.current_mode()[1])
        self.pwm_channels.blue.duty(64 * self.current_mode()[2])
        self.pwm_channels.red.freq(4)
        # this runs, but cannot be interrupted
        # uasyncio.run(control_animation())

    def next_adjustment(self):
        pass

    # TODO: generic deactivate in super-class
    def deactivate(self):
        print("party deactivate")
        # if self.task is not None:
        #    self.task.cancel()
        #    self.task = None
        self.pwm_channels.red.duty(0)
        self.pwm_channels.red.freq(60)
        self.pwm_channels.green.duty(0)
        self.pwm_channels.blue.duty(0)

