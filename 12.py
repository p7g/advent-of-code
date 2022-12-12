from aoc import *
import networkx
import string

height = dict(zip(string.ascii_lowercase, count()))
grid = [list(row) for row in data.splitlines()]
G = networkx.DiGraph()
start = end = None

for y in range(len(grid)):
    for x in range(len(grid[0])):
        c = grid[y][x]
        if c == "S":
            c = "a"
            start = (x, y)
        elif c == "E":
            c = "z"
            end = (x, y)
        h = height[c]
        for nbr in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            nx, ny = nbr
            if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
                continue
            nc = grid[ny][nx]
            if nc == "S":
                start = nbr
                nc = "a"
            elif nc == "E":
                nc = "z"
                end = nbr
            nh = height[nc]
            if nh <= h + 1:
                G.add_edge((x, y), nbr)

assert start is not None and end is not None

print(networkx.shortest_path_length(G, start, end))

a_squares = []
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] in "aS":
            a_squares.append((x, y))

print(min(networkx.shortest_path_length(G, pos, end) for pos in a_squares if networkx.has_path(G, pos, end)))
