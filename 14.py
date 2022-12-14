from aoc import *

sand_source = (500, 0)
paths = [[(int((ns := coord.split(","))[0]), int(ns[1])) for coord in l.split(" -> ")] for l in data.splitlines()]

minx, maxx = min(x for path in paths for x, y in path), max(x for path in paths for x, y in path)
miny, maxy = min(y for path in paths for x, y in path), max(y for path in paths for x, y in path)

stone_coords = set()
sand_coords = set()

for path in paths:
    for (ax, ay), (bx, by) in pairwise(path):
        if ax == bx:
            direction = sign(by - ay)
            for y in range(ay, by + direction, direction):
                stone_coords.add((ax, y))
        else:
            assert ay == by
            direction = sign(bx - ax)
            for x in range(ax, bx + direction, direction):
                stone_coords.add((x, ay))

blocked = lambda x, y: (x, y) in sand_coords or (x, y) in stone_coords or y == maxy + 2
had_first_soln = False

for unit in count(1):
    pos = sand_source

    while True:
        x, y = pos
        if not blocked(x, y + 1):
            pos = (x, y + 1)
        elif not blocked(x - 1, y + 1):
            pos = (x - 1, y + 1)
        elif not blocked(x + 1, y + 1):
            pos = (x + 1, y + 1)
        else:
            sand_coords.add(pos)
            break

    if not had_first_soln and pos[1] > maxy:
        had_first_soln = True
        print(unit - 1)
    elif sand_source in sand_coords:
        print(unit)
        break
