from rgb_duties_converter import RgbDutiesConverter, Duties


def test_white_to_duties():
    duties = RgbDutiesConverter.to_duties("#ffffff")
    expected_duties = Duties()
    expected_duties.white = 1020
    assert duties == expected_duties


def test_red_to_duties():
    duties = RgbDutiesConverter.to_duties("#ff0000")
    expected_duties = Duties()
    expected_duties.red = 1020
    assert duties == expected_duties
