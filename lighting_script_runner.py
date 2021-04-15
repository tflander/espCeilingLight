from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import uasyncio


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
            delay_time = command['time']
            delay_unit = command['unit']
            if delay_unit == 's':
                delay_time *= 1000
            elif delay_unit == 'm':
                delay_time *= 60000
            await uasyncio.sleep_ms(delay_time)
        elif command['command'] == 'fade':
            pass
            # 1) calculate difference between current value and desired value for each color
            # 2) calculate the number of fade steps based on the time/unit parameters and some constant (10ms?)
            # 3) calculate the value to add or subtract for each color for every fade step
            # 4) while not at desired color:
            #   adjust the current color based on step #3
            #   sleep for some constant (10ms?)

    @staticmethod
    def should_run_in_loop(commands):
        return 'sleep' in list(map(lambda command: command["command"], commands))
