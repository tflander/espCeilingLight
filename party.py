# TODO: move abstract stuff to a different library
from lighting_modes import *
import uasyncio

led_pwm_channels = LedPwmChannels(red_pin=21, green_pin=23, blue_pin=22, white_pin=19, uv_pin=18)


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
    while True:
        task = uasyncio.create_task(first_party_animation())
        await uasyncio.sleep(10)
        led_pwm_channels.zero_duty()
        task.cancel()
        task = uasyncio.create_task(second_party_animation())
        await uasyncio.sleep(10)
        led_pwm_channels.zero_duty()
        task.cancel()


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

