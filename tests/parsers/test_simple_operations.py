from parsers.expression_parser import parse_expression


def test_parse_addition():
    result = parse_expression("1    + 2")
    assert result.value == 3


def test_parse_multiplication():
    result = parse_expression("2 * 3")
    assert result.value == 6


def test_parse_division():
    result = parse_expression("10 / 2")
    assert result.value == 5


def test_parse_subtraction():
    result = parse_expression("2 - 3")
    assert result.value == -1


def test_exponents():
    result = parse_expression("2^3")
    assert result.value == 8


def test_parse_multiple_addition():
    result = parse_expression("1 + 2 + 3")
    assert result.value == 6


def test_parse_multiple_multiplication():
    result = parse_expression("2 * 3 * 4")
    assert result.value == 24


def test_parse_multiplication_with_addition():
    result = parse_expression("1 + 2 * 3 + 4")
    assert result.value == 11


def test_hex_math():
    result = parse_expression("0x0f * 10")
    assert result.value == 150

