import numpy as np
from math import gcd


def points_between(a, b):
    ax, ay = a
    bx, by = b

    # Calculate using A as origin
    bx -= ax
    by -= ay

    f = gcd(bx, by)
    dx = bx // f
    dy = by // f

    if dx == 0:
        ys = iter(range(0, by, np.sign(dy)))
        next(ys)
        return [(ax, y + ay) for y in ys]

    ps = []
    xs = iter(range(0, bx, dx))
    next(xs)
    for x in xs:
        y = (x * dy) // dx
        ps.append((x + ax, y + ay))

    return ps


def parse_points(data):
    ps = []
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line.strip()):
            if c == '#':
                ps.append((x, y))
    return ps
