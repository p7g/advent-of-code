from aoc import *

low_points = []

data = data.splitlines()
for y, row in enumerate(data):
    for x, height in enumerate(row):
        height = int(height)
        if y > 0 and height >= int(data[y - 1][x]):
            continue
        if y + 1 < len(data) and height >= int(data[y + 1][x]):
            continue
        if x > 0 and height >= int(data[y][x - 1]):
            continue
        if x + 1 < len(data[0]) and height >= int(data[y][x + 1]):
            continue
        low_points.append(height)


print(sum(p + 1 for p in low_points))


low_points = []

data = [list(map(int, l)) for l in data]
for y, row in enumerate(data):
    for x, height in enumerate(row):
        height = int(height)
        if y > 0 and height >= int(data[y - 1][x]):
            continue
        if y + 1 < len(data) and height >= int(data[y + 1][x]):
            continue
        if x > 0 and height >= int(data[y][x - 1]):
            continue
        if x + 1 < len(data[0]) and height >= int(data[y][x + 1]):
            continue
        low_points.append((x, y))


def adj(p):
    x, y = p
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


basins = []
for x, y in low_points:
    basin = {(x, y)}
    seen = {(x, y)}
    to_explore = adj((x, y))

    while to_explore:
        p = to_explore.pop()
        if p in seen:
            continue
        px, py = p
        if px < 0 or px >= len(data[0]):
            continue
        if py < 0 or py >= len(data):
            continue
        seen.add(p)
        if data[py][px] < 9:
            basin.add(p)
            to_explore.extend(adj(p))

    basins.append(basin)


biggest3 = sorted(basins, key=len, reverse=True)[:3]
print(reduce(mul, map(len, biggest3)))
