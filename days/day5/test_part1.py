import pytest
from lib.intcode import IntCodeVM
from lib.digits import digits, undigits


def test_intcode_io():
    vm = IntCodeVM([3, 0, 4, 0, 99])
    gen = vm.run()
    next(gen)
    assert gen.send(3) == 3


def test_undigits():
    for n in [12345, 54321, 11211, 91938]:
        assert undigits(digits(n)) == n


@pytest.mark.parametrize(
    "input,output",
    [
        (-1, 999),
        (3, 999),
        (8, 1000),
        (324, 1001),
    ],
)
def test_intcode_jump(input, output):
    vm = IntCodeVM.from_str(
        """
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
        """
    )
    gen = vm.run()
    next(gen)
    assert gen.send(input) == output
