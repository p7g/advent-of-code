from aoc import *

codes = data.splitlines()

keypad_coords = {}
for y, row in enumerate("789\n456\n123\n 0A".splitlines()):
    for x, c in enumerate(row):
        keypad_coords[c] = x, y

arrow_coords = {}
for y, row in enumerate(" ^A\n<v>".splitlines()):
    for x, c in enumerate(row):
        arrow_coords[c] = x, y

dtoarrow = {
    (0, 1): "v",
    (0, -1): "^",
    (1, 0): ">",
    (-1, 0): "<",
}


@cache
def possible_paths(src, dest, avoid):
    if src == dest:
        return [[src]]
    xsign, ysign = sign(dest[0] - src[0]), sign(dest[1] - src[1])
    paths = []
    if xsign:
        newsrc = src[0] + xsign, src[1]
        if newsrc != avoid:
            for path in possible_paths(newsrc, dest, avoid):
                paths.append([src, *path])
    if ysign:
        newsrc = src[0], src[1] + ysign
        if newsrc != avoid:
            for path in possible_paths(newsrc, dest, avoid):
                paths.append([src, *path])
    return paths


@cache
def min_presses(src, dest, robot, space=arrow_coords[" "]) -> int:
    if robot == 0:
        return abs(dest[0] - src[0]) + abs(dest[1] - src[1]) + 1
    min_ = None
    for path in possible_paths(src, dest, space):
        npresses = 0
        edges = ["A"] + [dtoarrow[b[0] - a[0], b[1] - a[1]] for a, b in pairwise(path)] + ["A"]
        for a, b in pairwise(edges):
            npresses += min_presses(arrow_coords[a], arrow_coords[b], robot - 1)
        if min_ is None or npresses < min_:
            min_ = npresses
    assert min_ is not None, (src, dest, space)
    return min_


for nrobots in (2, 25):
    s = 0
    for code in codes:
        n = 0
        src = "A"
        for digit in code:
            n += min_presses(
                keypad_coords[src], keypad_coords[digit], nrobots, keypad_coords[" "]
            )
            src = digit
        s += n * int(code[:-1])
    print(s)
