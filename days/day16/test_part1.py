import pytest
import numpy as np
from .day16lib import pattern, do_phases, do_phase, ones, read_input


@pytest.mark.parametrize("a,b", [(38, 8), (-17, 7), (7, 7)])
def test_ones(a, b):
    assert ones(a) == b


def test_do_phase():
    pat = pattern(8)
    input_ = np.asarray([1, 2, 3, 4, 5, 6, 7, 8], np.int8)
    input_ = do_phase(input_, pat)
    assert (input_ == np.asarray([4, 8, 2, 2, 6, 1, 5, 8], np.int8)).all()
    input_ = do_phase(input_, pat)
    assert (input_ == np.asarray([3, 4, 0, 4, 0, 4, 3, 8], np.int8)).all()
    input_ = do_phase(input_, pat)
    assert (input_ == np.asarray([0, 3, 4, 1, 5, 5, 1, 8], np.int8)).all()
    input_ = do_phase(input_, pat)
    assert (input_ == np.asarray([0, 1, 0, 2, 9, 4, 9, 8], np.int8)).all()


@pytest.mark.parametrize(
    "a,b",
    [
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ],
)
def test_do_phase_big_inputs(a, b):
    assert (do_phases(read_input(a), 100)[: len(b)] == read_input(b)).all()
