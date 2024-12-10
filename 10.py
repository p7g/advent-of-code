from aoc import *

map_ = [list(map(int, line)) for line in data.splitlines()]
W, H = wh(map_)

trailheads = []
for pt, height in pts(map_):
    if height == 0:
        trailheads.append(pt)

accessible_9s = defaultdict(Counter)

for trailhead in trailheads:
    positions = [trailhead]

    while positions:
        new_positions = []

        for position in positions:
            if position.get(map_) == 9:
                accessible_9s[trailhead][position] += 1
                continue

            for nbr in position.nbrs4((W, H)):
                if nbr.get(map_) != position.get(map_) + 1:
                    continue
                new_positions.append(nbr)

        positions = new_positions

print(sum(map(len, accessible_9s.values())))
print(sum(sum(c.values()) for c in accessible_9s.values()))
