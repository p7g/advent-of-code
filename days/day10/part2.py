import math
from collections import deque, defaultdict
from functools import partial
from os import path
from .day10lib import parse_points

coords = 11, 11


def angle(a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    ang = math.pi / 2 - math.atan2(-dy, dx)
    if ang < 0:
        ang += 2 * math.pi
    return ang


def distance(a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    return abs(dx) + abs(dy)


def key(a, b):
    return (angle(a, b), distance(a, b))


def destruction_order(o, ps):
    groups = defaultdict(deque)
    for p in sorted(filter(lambda p: p != o, ps), key=partial(key, o)):
        groups[angle(o, p)].append(p)
    groups = [kv[1] for kv in sorted(groups.items(), key=lambda kv: kv[0])]
    while any(groups):
        for ps in groups:
            if ps:
                yield ps.popleft()


def find_200th_asteroid(o, ps):
    ps = list(destruction_order(o, ps))
    return ps[199]


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    ps = parse_points(data)
    print(find_200th_asteroid((11, 11), ps))
