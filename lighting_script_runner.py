from animation_calculator import AnimationCalculator
from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import uasyncio
import math


class LightingScriptRunner:

    @staticmethod
    async def run(commands, led_pwm_channels: LedPwmChannels):
        run_in_loop = LightingScriptRunner.should_run_in_loop(commands)
        while True:
            for command in commands:
                await LightingScriptRunner.run_command(command, led_pwm_channels)
                if not run_in_loop:
                    break

    @staticmethod
    async def run_command(command, led_pwm_channels: LedPwmChannels):
        if command['command'] == 'setColor':
            duties = RgbDutiesConverter.to_duties(command['color'])
            led_pwm_channels.red.duty(duties.red)
            led_pwm_channels.green.duty(duties.green)
            led_pwm_channels.blue.duty(duties.blue)
            led_pwm_channels.white.duty(duties.white)
            led_pwm_channels.ultra_violet.duty(duties.ultra_violet)
        elif command['command'] == 'sleep':
            await uasyncio.sleep_ms(AnimationCalculator.delay_time_ms(command))
        elif command['command'] == 'fade':
            fade_params = AnimationCalculator.for_fade_command(command, led_pwm_channels)
            current_duties = led_pwm_channels.as_duties()
            target_color_duties = RgbDutiesConverter.to_duties(command['color'])

            # TODO: finish -- update pwm_channels
            duties_as_float = current_duties.to_rounded_int()  # TODO: use clone
            while current_duties != fade_params.target_color:
                duties_as_float.apply_deltas(fade_params.color_slice_deltas, target_color_duties)
                current_duties = duties_as_float.to_rounded_int()
                led_pwm_channels.set_from_duties(current_duties)
                await uasyncio.sleep_ms(fade_params.slice_duration_ms)

    @staticmethod
    def should_run_in_loop(commands):
        return 'sleep' in list(map(lambda command: command["command"], commands))
