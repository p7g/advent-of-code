import pytest
from .day4lib import digits, has_2_same_adjacent_digits


@pytest.mark.parametrize(
    "n,expected",
    [
        (112233, True),
        (123444, False),
        (111122, True),
    ],
)
def test_has_n_same_adjacent_digits(n, expected):
    assert has_2_same_adjacent_digits(digits(n)) is expected
