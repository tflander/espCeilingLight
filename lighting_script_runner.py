from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import uasyncio
import time

class LightingScriptRunner:

    @staticmethod
    async def run(commands, led_pwm_channels: LedPwmChannels):
        command = commands[0]
        print("LightingScriptRunner.run called")
        print(command)
        await LightingScriptRunner.run_command(command, led_pwm_channels)

    @staticmethod
    async def run_command(command, led_pwm_channels: LedPwmChannels):
        print("LightingScriptRunner.run_command called")
        print(command)
        if command['command'] == 'setColor':
            print("LightingScriptRunner.run_command called with command setColor")
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
            # TODO: await this?
            print(time.localtime())
            await uasyncio.sleep_ms(delay_time)  # returns singleton generator
            print(time.localtime())
