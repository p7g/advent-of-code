import pytest
from .day7lib import fwd, pipe
from .part1 import run_phase_setting


def test_fwd():
    def doubler():
        n = yield
        while True:
            n = yield n * 2

    def stringifier():
        n = yield
        while True:
            n = yield str(n)

    d = doubler()
    next(d)
    s = stringifier()
    next(s)
    fwdd = fwd([d, s])
    next(fwdd)

    assert list(pipe(range(5), fwdd)) == ["0", "2", "4", "6", "8"]


@pytest.mark.parametrize(
    "code,phase_setting,result",
    [
        (
            "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
            [4, 3, 2, 1, 0],
            43210,
        ),
        (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23"
            ",99,0,0",
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,"
            "1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
def test_run(code, phase_setting, result):
    assert run_phase_setting(code, phase_setting) == result
