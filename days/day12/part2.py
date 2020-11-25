from itertools import count
from math import gcd
from os.path import join, dirname
from .day12lib import parse_input, step


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def find_repeated_universe(moons):
    initx = [(m.x, m.vx) for m in moons]
    inity = [(m.y, m.vy) for m in moons]
    initz = [(m.z, m.vz) for m in moons]
    x = y = z = False
    period = 1

    for i in count(1):
        step(moons)
        if not x and [(m.x, m.vx) for m in moons] == initx:
            period = lcm(period, i)
            x = True
        if not y and [(m.y, m.vy) for m in moons] == inity:
            period = lcm(period, i)
            y = True
        if not z and [(m.z, m.vz) for m in moons] == initz:
            period = lcm(period, i)
            z = True
        if x and y and z:
            break

    return period


if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    print(find_repeated_universe(parse_input(data)))
