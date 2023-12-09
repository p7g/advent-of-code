from aoc import *

datasets = [list(map(int, line.split())) for line in data.splitlines()]


def x(data):
    if not any(data):
        return 0

    y = []
    for a, b in pairwise(data):
        y.append(b - a)

    return data[-1] + x(y)


print(sum(x(data) for data in datasets))


def x(data):
    if not any(data):
        return 0

    y = []
    for a, b in pairwise(data):
        y.append(b - a)

    return data[0] - x(y)


print(sum(x(data) for data in datasets))
