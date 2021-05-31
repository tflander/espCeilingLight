import re

from parsers.expression_parser import *


def test_addition():
    assert re.findall(addition_pattern, '12 + 34') == [' + ']


def test_positive_int():
    result = re.match(number_pattern, '12')
    assert result.group(1) == "12"


def test_positive_float():
    result = re.match(number_pattern, '12.34')
    assert result.group(1) == "12.34"


def test_negative_int():
    result = re.match(number_pattern, '-12')
    assert result.group(1) == "-12"


def test_negative_float():
    result = re.match(number_pattern, '-12.34')
    assert result.group(1) == "-12.34"
