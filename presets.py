from lighting_script_runner import LightingScriptRunner
from lighting_support import LedPwmChannels


class Presets:

    def __init__(self, pwm_channels: LedPwmChannels):
        self.pwm_channels = pwm_channels
        self.presets = []

    @staticmethod
    def select_next_preset():
        pass

    def add(self, commands):
        self.presets.append(commands)

    async def next(self):
        await LightingScriptRunner.run(self.presets[0], self.pwm_channels)
