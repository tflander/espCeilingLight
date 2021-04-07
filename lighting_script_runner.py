from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import uasyncio

class LightingScriptRunner:

    @staticmethod
    async def run(commands, led_pwm_channels: LedPwmChannels):
        command = commands[0]
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