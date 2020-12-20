from collections import Counter
from itertools import product
from lib.input import fetch
from math import sqrt
from operator import itemgetter

if __name__ == "__main__":
    data = fetch()
    tiles_data = data.strip().split("\n\n")

    tiles = []
    for t in tiles_data:
        idstr, *grid = t.strip().splitlines()
        id_ = int(idstr.split(" ")[1].rstrip(":"))

        gridl = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "#":
                    gridl[y][x] = 1

        tiles.append((id_, gridl))

    def edges(id_, grid):
        yield ("top", [grid[0][i] for i in range(len(grid[0]))])
        yield ("bottom", [grid[-1][i] for i in range(len(grid[0]))])
        yield ("left", [grid[i][0] for i in range(len(grid))])
        yield ("right", [grid[i][-1] for i in range(len(grid))])

    def top_edge(grid):
        return [grid[0][i] for i in range(len(grid[0]))]

    def bottom_edge(grid):
        return [grid[-1][i] for i in range(len(grid[0]))]

    def left_edge(grid):
        return [grid[i][0] for i in range(len(grid))]

    def right_edge(grid):
        return [grid[i][-1] for i in range(len(grid))]

    dirs = ["top", "right", "bottom", "left"]

    # The transform that must be applied to b
    def required_transform(a, b, b_rev=False):
        aidx = (dirs.index(a) + 2) % 4  # b needs to be 180deg from a
        bidx = dirs.index(b)
        val = aidx - bidx
        if val < 0:
            val = 4 - abs(val)
        mir = None
        if b_rev:
            if b in ("top", "bottom"):
                mir = "x"
            else:
                mir = "y"
        return (val % 4, mir)

    def do_transform(transform, b):
        rot, mir = transform
        if rot < 0:
            raise ValueError
        b2 = [b[i].copy() for i in range(len(b))]
        if mir:
            for y, row in enumerate(b):
                for x, c in enumerate(row):
                    if mir == "y":
                        b2[-(y + 1)][x] = c
                    else:
                        b2[y][-(x + 1)] = c
        if rot == 0:
            return b2
        b3 = [b2[i].copy() for i in range(len(b2))]
        for y in range(len(b2)):
            for x in range(len(b2[0])):
                b3[y][x] = b2[len(b2) - x - 1][y]
        rot -= 1
        if rot == 0:
            return b3
        return do_transform((rot, None), b3)

    def tile_str(id_, tile):
        s = f"Tile {id_}:\n"
        for row in tile:
            for c in row:
                s += "#" if c else "."
            s += "\n"
        return s

    def make_big_grid():
        return [[None] * dim for _ in range(dim)]

    def find_total_grid(total_grid, subgrids):
        if not subgrids:
            return total_grid
        for i, grid in enumerate(subgrids):
            for y, x in product(range(dim), range(dim)):
                if total_grid[y][x] is not None:
                    continue
                for rot, mir in product(range(4), [None, "x", "y"]):
                    g = do_transform((rot, mir), grid)
                    if (
                        (
                            x == 0
                            or total_grid[y][x - 1] is None
                            or left_edge(g) == right_edge(total_grid[y][x - 1])
                        )
                        and (
                            x + 1 == dim
                            or total_grid[y][x + 1] is None
                            or right_edge(g) == left_edge(total_grid[y][x + 1])
                        )
                        and (
                            y == 0
                            or total_grid[y - 1][x] is None
                            or top_edge(g) == bottom_edge(total_grid[y - 1][x])
                        )
                        and (
                            y + 1 == dim
                            or total_grid[y + 1][x] is None
                            or bottom_edge(g) == top_edge(total_grid[y + 1][x])
                        )
                    ):
                        new_total_grid = make_big_grid()
                        for y1, x1 in product(range(dim), range(dim)):
                            new_total_grid[y1][x1] = total_grid[y1][x1]
                        new_total_grid[y][x] = g
                        result = find_total_grid(
                            new_total_grid,
                            [g for j, g in enumerate(subgrids) if i != j],
                        )
                        if result is not None:
                            return result
        return None

    dim = int(sqrt(len(tiles)))
    tiles2 = tiles.copy()
    delta = {"top": (0, -1), "right": (1, 0), "bottom": (0, 1), "left": (-1, 0)}
    dest = {}
    streak = 0
    last_seen = None

    while tiles2:
        id_, grid = tiles2.pop()
        if not dest:
            dest[0, 0] = id_, grid
            dest[id_] = 0, 0
            continue
        possible = []
        for k, (id2, grid2) in dest.items():
            if not isinstance(k, tuple):
                continue
            assert id2 != id_
            for dir_, edge in edges(id_, grid):
                for dir2, edge2 in edges(id2, grid2):
                    if edge == edge2 or (rev := edge == list(reversed(edge2))):
                        dx, dy = delta[dir2]
                        x, y = dest[id2]
                        x += dx
                        y += dy
                        tr = required_transform(dir2, dir_, rev ^ (dir_ == dir2))
                        possible.append(((x, y), tr))

        xs = [p[0] for p in dest.keys() if isinstance(p, tuple)]
        ys = [p[1] for p in dest.keys() if isinstance(p, tuple)]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        possible = [
            ((x, y), tr)
            for (x, y), tr in possible
            if (
                (
                    minx <= x <= maxx
                    or (x > maxx and x - minx < dim)
                    or (x < minx and maxx - x < dim)
                )
                and (
                    miny <= y <= maxy
                    or (y > maxy and y - miny < dim)
                    or (y < miny and maxy - y < dim)
                )
            )
        ]

        points_dist = Counter(map(itemgetter(0), possible))
        for (x, y), n in points_dist.most_common():
            g = do_transform(next(tr for p, tr in possible if p == (x, y)), grid)
            matched = 0
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if (nx, ny) not in dest:
                    continue
                if nx < x and right_edge(dest[nx, ny][1]) != left_edge(g):
                    continue
                if nx > x and left_edge(dest[nx, ny][1]) != right_edge(g):
                    continue
                if ny < y and bottom_edge(dest[nx, ny][1]) != top_edge(g):
                    continue
                if ny > y and top_edge(dest[nx, ny][1]) != bottom_edge(g):
                    continue
                matched += 1
            if matched == n:
                dest[x, y] = id_, g
                dest[id_] = x, y
                break
        else:
            tiles2.insert(0, (id_, grid))
            if last_seen == len(tiles2):
                streak += 1
            else:
                streak = 0
                last_seen = len(tiles2)
            if streak == last_seen:
                break

    xs, ys = [], []
    for k in dest.keys():
        if isinstance(k, tuple):
            x, y = k
            xs.append(x)
            ys.append(y)

    total = make_big_grid()
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in dest:
                id_, g = dest[x, y]
                total[y - min(ys)][x - min(xs)] = g

    total = find_total_grid(total, [g for _, g in tiles2])

    if __debug__:
        for y in range(dim):
            for y2 in range(len(tiles[0][1])):
                for x in range(dim):
                    g = total[y][x]
                    print(
                        "".join(["#" if c else "." for c in g[y2]])
                        if g
                        else " " * len(tiles[0][1]),
                        end=" ",
                    )
                print()
            print()

    sidelen = len(tiles[0][1]) - 2  # remove 1 from all sides
    total_grid = [[0 for _ in range(sidelen * dim)] for _ in range(sidelen * dim)]

    for y in range(dim):
        for x in range(dim):
            grid = total[y][x]
            for y1 in range(1, sidelen + 1):
                for x1 in range(1, sidelen + 1):
                    total_grid[y * sidelen + y1 - 1][x * sidelen + x1 - 1] = grid[y1][
                        x1
                    ]

    pattern = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   \
""".splitlines()

    tr = (0, None)
    max_instances = 0
    for rot, mir in product(range(4), [None, "x", "y"]):
        grid = do_transform((rot, mir), total_grid)
        instances = []
        for y in range(0, sidelen * dim - len(pattern)):
            for x in range(sidelen * dim - len(pattern[0])):
                for py, prow in enumerate(pattern):
                    for px, c in enumerate(prow):
                        if c == "#" and not grid[y + py][x + px]:
                            break
                    else:
                        continue
                    break
                else:
                    instances.append((x, y))
        if len(instances) > max_instances:
            tr = (rot, mir)
            max_instances = len(instances)

    nxs = sum(c for row in total_grid for c in row if c)
    pnxs = sum(1 for row in pattern for c in row if c == "#")
    print(nxs - pnxs * max_instances)
