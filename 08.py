from aoc import *

grid = data.splitlines()
W, H = wh(grid)

locations = defaultdict(list)
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == ".":
            continue
        locations[c].append(Pt(x, y))

antinodes = set()

for antennae in locations.values():
    for (ax, ay), (bx, by) in product(antennae, repeat=2):
        if ax == bx and ay == by:
            continue
        dy, dx = by - ay, bx - ax
        antinode1 = Pt(ax - dx, ay - dy)
        antinode2 = Pt(bx + dx, by + dy)
        if antinode1.inbound((W, H)):
            antinodes.add(antinode1)
        if antinode2.inbound((W, H)):
            antinodes.add(antinode2)

print(len(antinodes))

antinodes = set()

for antennae in locations.values():
    for a, b in product(antennae, repeat=2):
        if a == b:
            continue
        d = b - a

        p = a
        while True:
            p2 = p - d
            if p2.x < 0 or p2.x >= W or p2.y < 0 or p2.y >= H:
                break
            p = p2

        while 0 <= p.x < W and 0 <= p.y < H:
            antinodes.add(p)
            p += d

print(len(antinodes))
