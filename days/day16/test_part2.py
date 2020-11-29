import pytest
from .day16lib import read_input
from .part2 import part2


@pytest.mark.parametrize(
    "input_,result",
    [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ],
)
def test_part2(input_, result):
    assert (part2(input_) == read_input(result)).all()
