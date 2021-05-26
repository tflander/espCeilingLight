import re


def test_foo():
    positive_number_pattern = '([0-9]+\\.?[0-9]*)'
    test_string = 'abyss'
    result = re.match(positive_number_pattern, test_string)

    assert 1 == 2
