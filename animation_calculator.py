from lighting_support import LedPwmChannels
from rgb_duties_converter import RgbDutiesConverter, Duties
import math


class FadeParams():

    def __init__(self, slice_duration_ms, target_color, color_total_deltas, color_slice_deltas):
        self.color_slice_deltas = color_slice_deltas
        self.color_total_deltas = color_total_deltas
        self.target_color = target_color
        self.slice_duration_ms = slice_duration_ms


class AnimationCalculator:
    @staticmethod
    def for_fade_command(command, led_pwm_channels: LedPwmChannels, slice_duration_ms = 10):
        target_color = RgbDutiesConverter.to_duties(command['color'])
        color_total_deltas = led_pwm_channels.delta_to_color(target_color)
        total_delay_ms = AnimationCalculator.delay_time_ms(command)
        slice_count = math.floor(total_delay_ms / slice_duration_ms)
        x = 0
        r = color_total_deltas.red / slice_count
        g = color_total_deltas.green / slice_count
        b = color_total_deltas.blue / slice_count
        w = color_total_deltas.white / slice_count
        u = color_total_deltas.ultra_violet / slice_count
        color_slice_deltas = Duties(r, g, b, w, u)

        return FadeParams(slice_duration_ms, target_color, color_total_deltas, color_slice_deltas)

    @staticmethod
    def delay_time_ms(command):
        delay_time = command['time']
        delay_unit = command['unit']
        if delay_unit == 's':
            delay_time *= 1000
        elif delay_unit == 'm':
            delay_time *= 60000
        return delay_time
