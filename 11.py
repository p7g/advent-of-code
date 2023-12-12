from aoc import *

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)

for i in range(h - 1, -1, -1):
    if all(c == "." for c in grid[i]):
        grid.insert(i, ["."] * w)

w, h = wh(grid)

for i in range(w - 1, -1, -1):
    for j in range(h):
        if grid[j][i] == "#":
            break
    else:
        for j in range(h):
            grid[j].insert(i, ".")

w, h = wh(grid)
galaxies = {(x, y) for y in range(h) for x in range(w) if grid[y][x] == "#"}
print(
    sum(abs(ax - bx) + abs(ay - by) for (ax, ay), (bx, by) in combinations(galaxies, 2))
)

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)
expanded_rows = [i for i in range(h) if all(c == "." for c in grid[i])]
expanded_cols = [i for i in range(w) if all(grid[j][i] == "." for j in range(h))]
galaxies = set()

y_expansions = 0
for y in range(h):
    if y in expanded_rows:
        y_expansions += 1
        continue
    x_expansions = 0
    for x in range(w):
        if x in expanded_cols:
            x_expansions += 1
            continue
        if grid[y][x] == "#":
            galaxies.add((x + x_expansions * 999_999, y + y_expansions * 999_999))

print(
    sum(abs(ax - bx) + abs(ay - by) for (ax, ay), (bx, by) in combinations(galaxies, 2))
)
