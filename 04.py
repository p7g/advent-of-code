from aoc import *

grid = data.splitlines()
dims = wh(grid)

n = 0
for pt, c in pts(grid):
    if c == ".":
        continue

    adj = 0
    for nbr in pt.nbrs8(dims):
        if nbr.get(grid) == "@":
            adj += 1

    n += adj < 4
print(n)


grid = [list(row) for row in grid]
removed = 0
while True:
    n = 0
    for pt, c in pts(grid):
        if c == ".":
            continue

        adj = 0
        for nbr in pt.nbrs8(dims):
            if nbr.get(grid) == "@":
                adj += 1

        if adj < 4:
            n += 1
            pt.set(grid, ".")

    if n == 0:
        break
    removed += n

print(removed)
