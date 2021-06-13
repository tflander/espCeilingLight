import re

from parsers.expression_parser import *


def test_addition():
    assert re.findall(addition_pattern, '+ 34') == ['+ ']


def test_multiplication():
    assert re.findall(multiplication_pattern, '* 34') == ['* ']


def test_division():
    assert re.findall(division_pattern, '/ 34') == ['/ ']


def test_subtraction():
    assert re.findall(subtraction_pattern, '- 34') == ['- ']


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


def test_hex():
    result = re.match(hex_number_pattern, '0x0f')
    assert result.group(1) == "0x0f"


def test_variable_identifier():
    result = re.match(variable_identifier_pattern, 'some_variableName10=0')
    assert result.group(1) == "some_variableName10"


def test_left_paren():
    result = re.match(left_paren_pattern, '( x + 1)')
    assert result.group(1) == "( "


def test_right_paren():
    result = re.match(right_paren_pattern, ') + 3')
    assert result.group(1) == ") "
