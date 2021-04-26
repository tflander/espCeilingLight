import asyncio
import pytest

from duties import Duties
from presets import Presets


@pytest.fixture()
def presets():
    presets = Presets()

    preset1 = [{"command": "setColor", "color": "#ff0000"}]
    presets.add(preset1)
    preset2 = [{"command": "setColor", "color": "#00ff00"}]
    presets.add(preset2)
    preset3 = [{"command": "setColor", "color": "#0000ff"}]
    presets.add(preset3)
    return presets


def test_add_preset(presets):
    expected_presets = [
        [{"command": "setColor", "color": "#ff0000"}],
        [{"command": "setColor", "color": "#00ff00"}],
        [{"command": "setColor", "color": "#0000ff"}]
    ]
    assert presets.presets == expected_presets


def test_next_preset_cycles(presets):

    assert presets.next() == [{"command": "setColor", "color": "#ff0000"}]
    assert presets.next() == [{"command": "setColor", "color": "#00ff00"}]
    assert presets.next() == [{"command": "setColor", "color": "#0000ff"}]
    assert presets.next() == [{"command": "setColor", "color": "#ff0000"}]
    assert presets.next() == [{"command": "setColor", "color": "#00ff00"}]
    assert presets.next() == [{"command": "setColor", "color": "#0000ff"}]
