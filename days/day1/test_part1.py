import pytest
from .day1lib import fuel_req


@pytest.mark.parametrize(
    "mass,expected",
    [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ]
)
def test_fuel_req(mass, expected):
    assert fuel_req(mass) == expected
