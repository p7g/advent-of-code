import pytest
from .day4lib import (
    digits,
    has_no_decreasing_digits,
    has_same_adjacent_digits,
)
from .part1 import suitable


@pytest.mark.parametrize(
    "n,digs",
    [
        (12345, [1, 2, 3, 4, 5]),
        (54321, [5, 4, 3, 2, 1]),
        (10001, [1, 0, 0, 0, 1]),
    ],
)
def test_digits(n, digs):
    assert digits(n) == digs


@pytest.mark.parametrize(
    "n,expected",
    [
        (12345, True),
        (54321, False),
        (11111, True),
        (669796, False),
    ],
)
def test_has_no_decreasing_digits(n, expected):
    assert has_no_decreasing_digits(digits(n)) is expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (12345, False),
        (12234, True),
        (11111, True),
    ],
)
def test_has_same_adjacent_digits(n, expected):
    assert has_same_adjacent_digits(digits(n)) is expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (111111, True),
        (223450, False),
        (123789, False),
    ],
)
def test_part1(n, expected):
    assert suitable(digits(n)) is expected
