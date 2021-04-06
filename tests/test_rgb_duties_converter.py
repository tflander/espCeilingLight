from rgb_duties_converter import RgbDutiesConverter, Duties
import pytest


@pytest.mark.parametrize("test_name, rgb_string, expected_duties", [
    ("pure red", "#ff0000", Duties(red=1020)),
    ("pure green", "#00ff00", Duties(green=1020)),
    ("pure blue", "#0000ff", Duties(blue=1020)),
    ("pure white", "#ffffff", Duties(white=1020)),
    ("pure cyan", "#00ffff", Duties(green=1020, blue=1020)),
    ("pure magenta", "#ff00ff", Duties(red=1020, blue=1020)),
    ("pure yellow", "#ffff00", Duties(red=1020, green=1020)),
    ("dim red", "#660000", Duties(red=408)),
    ("dim green", "#006600", Duties(green=408)),
    ("dim blue", "#000066", Duties(blue=408)),
    ("dim white", "#666666", Duties(white=408)),
    ("bright red", "#ff6666", Duties(red=612, white=408)),
    ("bright green", "#66ff66", Duties(green=612, white=408)),
    ("bright blue", "#6666ff", Duties(blue=612, white=408)),
    ("bright cyan", "#66ffff", Duties(green=612, blue=612, white=408)),
    ("bright magenta", "#ff66ff", Duties(red=612, blue=612, white=408)),
    ("bright yellow", "#ffff66", Duties(red=612, green=612, white=408)),
])
def test_to_duties(test_name, rgb_string, expected_duties):
    duties = RgbDutiesConverter.to_duties(rgb_string)
    assert duties == expected_duties


def test_to_duties_requires_a_valid_color():
    with pytest.raises(ValueError):
        RgbDutiesConverter.to_duties("this is not a color")


def test_valid_color():
    assert RgbDutiesConverter.is_valid_color("#aabbcc")


def test_valid_color_starts_with_hash():
    assert not RgbDutiesConverter.is_valid_color("aabbcc")


def test_valid_colors_are_three_bytes():
    assert not RgbDutiesConverter.is_valid_color("#aabbccdd")


def test_valid_colors_are_hex():
    assert not RgbDutiesConverter.is_valid_color("#xxyyzz")
