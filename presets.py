from lighting_script_runner import LightingScriptRunner
from lighting_support import LedPwmChannels


class Presets:

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.presets = []
        self.current_preset = -1

    @staticmethod
    def select_next_preset():
        pass

    def add(self, commands):
        self.presets.append(commands)

    async def next(self):
        self.current_preset += 1
        if self.current_preset >= len(self.presets):
            self.current_preset = 0
        await LightingScriptRunner.run(self.presets[self.current_preset], self.pwm_channels)
