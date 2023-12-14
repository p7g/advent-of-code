from aoc import *

grid = [list(line) for line in data.splitlines()]

for y, row in enumerate(grid):
    if y == 0:
        continue

    for x, c in enumerate(row):
        if c != "O":
            continue

        y2 = y - 1
        for y2 in range(y - 1, -2, -1):
            if grid[y2][x] in "O#":
                break

        if y2 != y - 1:
            grid[y2 + 1][x] = "O"
            grid[y][x] = "."

print(sum(len(grid) - y for y, row in enumerate(grid) for c in row if c == "O"))

grid = [list(line) for line in data.splitlines()]
states = {}
states_by_i = {}

for i in count():
    state = "\n".join("".join(row) for row in grid)
    if state in states:
        cycle_start = states[state]
        cycle_length = i - states[state]

        s = (4_000_000_000 - cycle_start) % cycle_length

        print(sum(len(grid) - y for y, row in enumerate(states_by_i[s + cycle_start].splitlines()) for c in row if c == "O"))
        break
    else:
        states[state] = i
        states_by_i[i] = state

    if i % 4 == 0:
        for y, row in enumerate(grid):
            if y == 0:
                continue

            for x, c in enumerate(row):
                if c != "O":
                    continue

                y2 = y - 1
                for y2 in range(y - 1, -2, -1):
                    if y2 != -1 and grid[y2][x] in "O#":
                        break

                if y2 != y - 1:
                    grid[y2 + 1][x] = "O"
                    grid[y][x] = "."
    elif i % 4 == 1:
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if x == 0:
                    continue
                elif c != "O":
                    continue

                x2 = x - 1
                for x2 in range(x - 1, -2, -1):
                    if x2 != -1 and grid[y][x2] in "O#":
                        break

                if x2 != x - 1:
                    grid[y][x2 + 1] = "O"
                    grid[y][x] = "."
    elif i % 4 == 2:
        for y, row in reversed(list(enumerate(grid))):
            if y == len(grid) - 1:
                continue

            for x, c in enumerate(row):
                if c != "O":
                    continue

                y2 = y + 1
                for y2 in range(y + 1, len(grid) + 1):
                    if y2 != len(grid) and grid[y2][x] in "O#":
                        break

                if y2 != y + 1:
                    grid[y2 - 1][x] = "O"
                    grid[y][x] = "."
    elif i % 4 == 3:
        for y, row in enumerate(grid):
            for x, c in reversed(list(enumerate(row))):
                if x == len(grid[0]) - 1:
                    continue
                elif c != "O":
                    continue

                x2 = x + 1
                for x2 in range(x + 1, len(grid[0]) + 1):
                    if x2 != len(grid[0]) and grid[y][x2] in "O#":
                        break

                if x2 != x + 1:
                    grid[y][x2 - 1] = "O"
                    grid[y][x] = "."
