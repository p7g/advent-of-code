import numpy as np
from itertools import cycle


def read_input(input_, n=1):
    len_ = len(input_) * n
    return np.fromiter(cycle(map(int, input_)), np.int8, len_)


def ones(n):
    return abs(n) % 10


def apply_pattern_column(arr, col):
    offset = 1
    i, j = 0, 0
    while True:
        for x in [0, 1, 0, -1]:
            for _ in range(col + 1):
                if i >= len(arr):
                    return
                if j >= offset:
                    arr[i] = x
                    i += 1
                j += 1


def pattern(len_):
    arr = np.zeros((len_, len_), np.int8, order="F")
    for x in range(len_):
        apply_pattern_column(arr[x], x)
    return arr


def do_phase(input_, pattern):
    return ones(pattern @ input_)


def do_phases(input_, n):
    pat = pattern(len(input_))
    for _ in range(n):
        input_ = do_phase(input_, pat)
    return input_
