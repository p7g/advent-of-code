from aoc import *

ns = [int("".join(n)) * (-1 if d == "L" else 1) for d, *n in data.splitlines()]

z = 0
v = 50
for n in ns:
    v += n
    v %= 100
    z += v == 0

print(z)


z = 0
v = 50
for n in ns:
    if n > 0:
        x, v = divmod(v + n, 100)
        z += x
    else:
        x, y = divmod(n, -100)
        z += x
        z += abs(y) >= v and v != 0
        v += y
        v %= 100

print(z)
