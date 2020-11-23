import pytest
from .part2 import fuel_req_rec


@pytest.mark.parametrize(
    "fuel,result",
    [
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ],
)
def test_fuel_fuel(fuel, result):
    assert fuel_req_rec(fuel) == result
