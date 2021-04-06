from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter


class LightingScriptRunner:

    @staticmethod
    def run(commands, led_pwm_channels: LedPwmChannels):
        command = commands[0]
        duties = RgbDutiesConverter.to_duties(command['color'])
        led_pwm_channels.red.duty(duties.red)
        led_pwm_channels.green.duty(duties.green)
        led_pwm_channels.blue.duty(duties.blue)
        led_pwm_channels.white.duty(duties.white)
        led_pwm_channels.ultra_violet.duty(duties.ultra_violet)
