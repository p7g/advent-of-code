from aoc import *


# https://www.sciencedirect.com/science/article/pii/S0166218X14000080
def do_solve(viz, numbers):
    global partial_colouring, d, sol

    n, k = len(viz), len(numbers)
    partial_colouring = list(viz)
    partial_colouring.insert(0, None)
    d = [0, *numbers]
    sol = [[-1] * len(d) for _ in range(len(partial_colouring))]

    return solve(n, k)


def solve(i, j):
    if i < 0 or j < 0:
        return 0
    elif i == j == 0:
        return 1
    if sol[i][j] != -1:
        return sol[i][j]
    else:
        sol[i][j] = 0
        if partial_colouring[i] != "#":
            sol[i][j] += solve(i - 1, j)
        if can_place_block(i, j):
            sol[i][j] += solve(i - d[j] - (j > 1), j - 1)
        return sol[i][j]


def can_place_block(i, j):
    for m in range(i, i - d[j], -1):
        if partial_colouring[m] == ".":
            return False
    if j > 1 and partial_colouring[i - d[j]] == "#":
        return False
    return True


s = 0
for line in data.splitlines():
    visualization, numbers_raw = line.split(None, 1)
    numbers = [int(x) for x in numbers_raw.split(',')]
    s += do_solve(visualization, numbers)
print(s)

s = 0
for line in data.splitlines():
    visualization, numbers_raw = line.split(None, 1)
    visualization = "?".join([visualization] * 5)
    numbers_raw = ",".join([numbers_raw] * 5)
    numbers = [int(x) for x in numbers_raw.split(',')]
    s += do_solve(visualization, numbers)
print(s)
