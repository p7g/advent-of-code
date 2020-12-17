from lib.input import fetch_lines
from operator import itemgetter

if __name__ == "__main__":
    data = fetch_lines()
    grid = list(map(str.strip, data))

    def nbrs(n):
        x, y, z = n
        for x2 in [x - 1, x, x + 1]:
            for y2 in [y - 1, y, y + 1]:
                for z2 in [z - 1, z, z + 1]:
                    if (x2, y2, z2) == n:
                        continue
                    yield x2, y2, z2

    active = set()
    for y, xs in enumerate(grid):
        for x, c in enumerate(xs):
            if c == "#":
                active.add((x, y, 0))

    for _ in range(6):
        minx, miny, minz = (
            min(map(itemgetter(0), active)),
            min(map(itemgetter(1), active)),
            min(map(itemgetter(2), active)),
        )
        maxx, maxy, maxz = (
            max(map(itemgetter(0), active)),
            max(map(itemgetter(1), active)),
            max(map(itemgetter(2), active)),
        )

        new_active = set()

        for z in range(minz - 1, maxz + 2):
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    n = x, y, z
                    if n in active:
                        if sum(nbr in active for nbr in nbrs(n)) in (2, 3):
                            new_active.add(n)

                    if n not in active:
                        if sum(nbr in active for nbr in nbrs(n)) == 3:
                            new_active.add(n)

        active = new_active

    print(len(active))
