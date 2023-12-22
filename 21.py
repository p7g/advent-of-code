from aoc import *

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)
start = next(pt for pt, c in pts(grid) if c == "S")

positions = {start}
distance = {start: 0}

while positions:
    new_positions = set()
    for pos in positions:
        for nbr in pos.nbrs4((w, h)):
            if nbr.inbound((w, h)):
                if nbr.get(grid) == "#" or nbr in distance:
                    continue
                new_positions.add(nbr)
                distance[nbr] = distance[pos] + 1
    positions = new_positions

print(sum(d % 2 == 0 for d in distance.values() if d <= 64))

grid = [["." if c == "S" else c for c in row] * 5 for row in grid * 5]
w, h = wh(grid)
start = Pt(w // 2, h // 2)

positions = {start}
distance = {start: 0}
ss = []

for i in range(328):
    new_positions = set()
    for pos in positions:
        for nbr in pos.nbrs4((w, h)):
            if nbr.inbound((w, h)):
                if nbr.get(grid) == "#" or nbr in distance:
                    continue
                new_positions.add(nbr)
                distance[nbr] = distance[pos] + 1
    positions = new_positions

    if (i - 65) % 131 == 0:
        ss.append(sum(d % 2 == i % 2 for d in distance.values() if d <= i))

# stolen from https://gist.github.com/dllu/0ca7bfbd10a199f69bcec92f067ec94c
import numpy as np
vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
x = np.linalg.solve(vandermonde, ss).astype(np.int64)
n = (26501365 - 65) // 131
print(x[0] * n ** 2 + x[1] * n + x[2])
