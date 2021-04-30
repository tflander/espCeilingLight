from animation_calculator import AnimationCalculator
from led_pwm_channels import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import uasyncio
import math


class LightingScriptRunner:

    @staticmethod
    async def run(commands, led_pwm_channels: LedPwmChannels):
        print("LightingScriptRunner.run called")
        run_in_loop = LightingScriptRunner.should_run_in_loop(commands)
        while True:
            for command in commands:
                await LightingScriptRunner.run_command(command, led_pwm_channels)
            if not run_in_loop:
                break

    @staticmethod
    async def run_command(command, led_pwm_channels: LedPwmChannels):
        if command.startswith('#'):
            duties = RgbDutiesConverter.to_duties(command)
            led_pwm_channels.red.duty(duties.red)
            led_pwm_channels.green.duty(duties.green)
            led_pwm_channels.blue.duty(duties.blue)
            led_pwm_channels.white.duty(duties.white)
            led_pwm_channels.ultra_violet.duty(duties.ultra_violet)
        elif command.startswith('sleep'):
            parts = command.split()
            await uasyncio.sleep_ms(round(AnimationCalculator.delay_time_ms(parts[1])))
        elif command.startswith('fade'):
            parts = command.split()
            target_color_duties = RgbDutiesConverter.to_duties(parts[3])
            fade_params = AnimationCalculator.for_fade_command(target_color_duties, parts[1], led_pwm_channels)
            current_duties = led_pwm_channels.as_duties()

            duties_as_float = current_duties
            while current_duties != fade_params.target_color:
                duties_as_float.apply_deltas(fade_params.color_slice_deltas, target_color_duties)
                current_duties = duties_as_float.to_rounded_int()
                led_pwm_channels.set_from_duties(current_duties)
                await uasyncio.sleep_ms(fade_params.slice_duration_ms)

    @staticmethod
    def should_run_in_loop(commands):
        command_verbs = list(map(lambda command: command.split()[0], commands))
        return 'sleep' in command_verbs or 'fade' in command_verbs
