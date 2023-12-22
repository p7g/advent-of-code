from aoc import *

ids = count()
bricks = []
for line in data.splitlines():
    p1, p2 = line.split("~", 1)
    p1 = tuple(map(int, p1.split(",")))
    p2 = tuple(map(int, p2.split(",")))
    bricks.append((p1, p2, next(ids)))

xs, ys, zs = zip(*(point for brick in bricks for point in brick[:-1]))
maxx, maxy, maxz = max(xs), max(ys), max(zs)
grid = [
    [[None for _ in range(maxx + 1)] for _ in range(maxy + 1)] for _ in range(maxz + 2)
]
for y in range(maxy + 1):
    for x in range(maxx + 1):
        grid[0][y][x] = "-"

landed = set()
falling = set(bricks)
while falling:
    (x1, y1, z1), (x2, y2, z2), id_ = min(
        falling, key=lambda brick: min(brick[0][2], brick[1][2])
    )
    falling.remove(((x1, y1, z1), (x2, y2, z2), id_))

    bottom_z = min(z1, z2)
    distance = 0
    while bottom_z - distance - 1 >= 0:
        if any(
            grid[bottom_z - distance - 1][y][x] is not None
            for y in range(min(y1, y2), max(y1, y2) + 1)
            for x in range(min(x1, x2), max(x1, x2) + 1)
        ):
            break
        distance += 1

    z1 -= distance
    z2 -= distance

    for z, y, x in product(
        range(min(z1, z2), max(z1, z2) + 1),
        range(min(y1, y2), max(y1, y2) + 1),
        range(min(x1, x2), max(x1, x2) + 1),
    ):
        grid[z][y][x] = id_

    landed.add(((x1, y1, z1), (x2, y2, z2), id_))

in_edges = defaultdict(set)
out_edges = defaultdict(set)
xs, ys, zs = zip(*(point for brick in landed for point in brick[:-1]))
maxx, maxy, maxz = max(xs), max(ys), max(zs)

for z in range(maxz, 0, -1):
    for y in range(maxy, -1, -1):
        for x in range(maxx, -1, -1):
            block_here = grid[z][y][x]
            if block_here is None:
                continue
            block_below = grid[z - 1][y][x]
            if block_below is None or block_below == "-" or block_below == block_here:
                continue
            in_edges[block_below].add(block_here)
            out_edges[block_here].add(block_below)

can_disintegrate = set()
for p1, p2, node in landed:
    if not in_edges[node]:
        can_disintegrate.add(node)
    elif all(len(out_edges[nbr]) > 1 for nbr in in_edges[node]):
        can_disintegrate.add(node)

print(len(can_disintegrate))

min_z_by_id = {id_: min(p1[2], p2[2]) for p1, p2, id_ in landed}
s = 0

for p1, p2, node in landed:
    work = [(min_z_by_id[node], node)]
    heapify(work)
    fallen = set()

    while work:
        _minz, node = heappop(work)
        fallen.add(node)
        for nbr in in_edges[node]:
            if all(nbr2 in fallen for nbr2 in out_edges[nbr]):
                heappush(work, (min_z_by_id[nbr], nbr))

    s += len(fallen) - 1

print(s)
