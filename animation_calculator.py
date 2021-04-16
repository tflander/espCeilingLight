from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter
import math


class AnimationCalculator:
    @staticmethod
    def for_fade_command(command, led_pwm_channels: LedPwmChannels):
        slice_duration_ms = 10
        target_color = RgbDutiesConverter.to_duties(command['color'])
        color_deltas = led_pwm_channels.delta_to_color(target_color)
        total_delay_ms = AnimationCalculator.delay_time_ms(command)
        slice_count = math.floor(total_delay_ms / slice_duration_ms)
        x = 0
        # 3) calculate the value to add or subtract for each color for every fade step

    @staticmethod
    def delay_time_ms(command):
        delay_time = command['time']
        delay_unit = command['unit']
        if delay_unit == 's':
            delay_time *= 1000
        elif delay_unit == 'm':
            delay_time *= 60000
        return delay_time
