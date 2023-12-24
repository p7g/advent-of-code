import z3
from aoc import *

Pt = namedtuple("Pt", "x,y,z")
zone_min, zone_max = 200000000000000, 400000000000000

hailstones = []
for line in data.splitlines():
    pt, v = line.replace(",", "").split(" @ ", 1)
    pt = Pt(*map(int, pt.split()))
    v = Pt(*map(int, v.split()))
    hailstones.append((pt, v))

n_collisions = 0
for (pt1, v1), (pt2, v2) in combinations(hailstones, 2):
    v2perp = (-v2.y, v2.x)
    dp = reduce(lambda n, x: n + x[0] * x[1], zip(v1[:2], v2perp), 1)
    if dp == 0:
        continue

    a = v1.y / v1.x
    c = pt1.y - a * pt1.x
    b = v2.y / v2.x
    d = pt2.y - b * pt2.x
    if a - b == 0:
        continue
    x = (d - c) / (a - b)
    y = a * x + c

    t = (x - pt1.x) / v1.x
    s = (x - pt2.x) / v2.x
    if t < 0 or s < 0:
        continue

    n_collisions += zone_min <= x <= zone_max and zone_min <= y <= zone_max

print(n_collisions)

x, y, z = z3.RealVector("p", 3)
vx, vy, vz = z3.RealVector("v", 3)
t1, t2, t3 = z3.RealVector("t", 3)
h1, h2, h3 = hailstones[:3]

solver = z3.Solver()

solver.add(h1[0].x + h1[1].x * t1 == x + vx * t1)
solver.add(h1[0].y + h1[1].y * t1 == y + vy * t1)
solver.add(h1[0].z + h1[1].z * t1 == z + vz * t1)

solver.add(h2[0].x + h2[1].x * t2 == x + vx * t2)
solver.add(h2[0].y + h2[1].y * t2 == y + vy * t2)
solver.add(h2[0].z + h2[1].z * t2 == z + vz * t2)

solver.add(h3[0].x + h3[1].x * t3 == x + vx * t3)
solver.add(h3[0].y + h3[1].y * t3 == y + vy * t3)
solver.add(h3[0].z + h3[1].z * t3 == z + vz * t3)

solver.check()
print(solver.model().eval(x + y + z))
