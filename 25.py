from aoc import *

data2 = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()

grid = [list(row) for row in data.splitlines()]
H = len(grid)
W = len(grid[0])

for step in count(1):
    moves = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == ">":
                x2 = x + 1 if x + 1 < W else 0
                if grid[y][x2] != ".":
                    continue
                moves.append(((x, y), (x2, y)))

    had_east_moves = bool(moves)
    for (x1, y1), (x2, y2) in moves:
        grid[y2][x2] = grid[y1][x1]
        grid[y1][x1] = "."

    moves = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "v":
                y2 = y + 1 if y + 1 < H else 0
                if grid[y2][x] != ".":
                    continue
                moves.append(((x, y), (x, y2)))

    for (x1, y1), (x2, y2) in moves:
        grid[y2][x2] = grid[y1][x1]
        grid[y1][x1] = "."

    if not moves and not had_east_moves:
        break

print(step)
