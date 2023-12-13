from aoc import *

patterns = data.split("\n\n")
mirror_points = []

s = 0
for pattern in patterns:
    grid = pattern.splitlines()
    w, h = wh(grid)

    mirror_point = None

    for y, (a, b) in enumerate(pairwise(grid)):
        if a != b:
            continue

        for i in range(1, min(y + 1, h - y - 1)):
            a, b = grid[y - i], grid[y + i + 1]
            if a != b:
                break
        else:
            mirror_point = ("horizontal", y)

    if mirror_point is None:
        for x in range(w - 1):
            a = [line[x] for line in grid]
            b = [line[x + 1] for line in grid]
            if a != b:
                continue

            for i in range(1, min(x + 1, w - x - 1)):
                a = [line[x - i] for line in grid]
                b = [line[x + i + 1] for line in grid]
                if a != b:
                    break
            else:
                mirror_point = ("vertical", x)

    assert mirror_point is not None
    orientation, n = mirror_point
    s += (n + 1) * (1 if orientation == "vertical" else 100)
print(s)


def reflects_horizontally(grid, y, i, did_edit=False):
    if i == y + 1 or i == len(grid) - y - 1:
        return did_edit

    a, b = grid[y - i], grid[y + i + 1]
    if a == b:
        return reflects_horizontally(grid, y, i + 1, did_edit)
    elif sum(aa != bb for aa, bb in zip(a, b)) == 1:
        grid2 = [line[:] for line in grid]
        grid3 = [line[:] for line in grid]
        pos = next(i for i, (aa, bb) in enumerate(zip(a, b)) if aa != bb)
        grid2[y - i][pos] = b[pos]
        grid3[y + i + 1][pos] = a[pos]
        return reflects_horizontally(grid2, y, i + 1, True) or reflects_horizontally(grid3, y, i + 1, True)
    else:
        return False


def reflects_vertically(grid, x, i, did_edit=False):
    if i == x + 1 or i == len(grid[0]) - x - 1:
        return did_edit

    a = [line[x - i] for line in grid]
    b = [line[x + i + 1] for line in grid]
    if a == b:
        return reflects_vertically(grid, x, i + 1, did_edit)
    elif sum(aa != bb for aa, bb in zip(a, b)) == 1:
        grid2 = [line[:] for line in grid]
        grid3 = [line[:] for line in grid]
        pos = next(i for i, (aa, bb) in enumerate(zip(a, b)) if aa != bb)
        grid2[pos][x - i] = b[pos]
        grid3[pos][x + i + 1] = a[pos]
        return reflects_vertically(grid2, x, i + 1, True) or reflects_vertically(grid3, x, i + 1, True)
    else:
        return False


s = 0
for pattern in patterns:
    grid = [list(line) for line in pattern.splitlines()]
    w, h = wh(grid)

    mirror_point = None

    for y, (a, b) in enumerate(pairwise(grid)):
        if reflects_horizontally(grid, y, 0):
            mirror_point = ("horizontal", y)
            break

    if mirror_point is None:
        for x in range(w - 1):
            if reflects_vertically(grid, x, 0):
                mirror_point = ("vertical", x)
                break

    assert mirror_point is not None
    orientation, n = mirror_point
    s += (n + 1) * (1 if orientation == "vertical" else 100)
print(s)
