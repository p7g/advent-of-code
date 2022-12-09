from aoc import *

grid = [list(map(int, row)) for row in data.splitlines()]

nvisible = 0
for y, row in enumerate(grid):
    for x, height in enumerate(row):
        if y == 0 or y == len(grid) - 1:
            visible = True
        elif x == 0 or x == len(grid[0]) - 1:
            visible = True
        elif all(grid[y2][x] < height for y2 in range(y + 1, len(grid))):
            visible = True
        elif all(grid[y2][x] < height for y2 in range(0, y)):
            visible = True
        elif all(grid[y][x2] < height for x2 in range(x + 1, len(grid[0]))):
            visible = True
        elif all(grid[y][x2] < height for x2 in range(0, x)):
            visible = True
        else:
            visible = False

        nvisible += visible

print(nvisible)


def vis(pos, dx=0, dy=0):
    x, y = pos
    h = grid[y][x]
    n = 0

    while True:
        x += dx
        y += dy
        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            break
        n += 1
        if h <= grid[y][x]:
            break

    return n


def scenic_scores():
    for y, row in enumerate(grid):
        if y == 0 or y == len(grid) - 1:
            continue

        for x in range(len(row)):
            if x == 0 or x == len(grid[0]) - 1:
                continue

            yield vis((x, y), dx=1) * vis((x, y), dx=-1) * vis((x, y), dy=1) * vis((x, y), dy=-1)


print(max(scenic_scores()))
