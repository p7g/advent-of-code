import sys
from aoc import *

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)
start = one(Pt(x, 0) for x in range(w) if grid[0][x] == ".")
end = one(Pt(x, h - 1) for x in range(w) if grid[h - 1][x] == ".")
directions = {">": Pt(1, 0), "<": Pt(-1, 0), "^": Pt(0, -1), "v": Pt(0, 1)}
seen = set()
undefined = object()

sys.setrecursionlimit(sys.getrecursionlimit() * 10)


def search(pos, ignore_slopes=False):
    longest = undefined
    for nbr in (
        pos.nbrs4()
        if pos.get(grid) == "." or ignore_slopes
        else [pos + directions[pos.get(grid)]]
    ):
        c = nbr.get(grid)
        if c == "#":
            continue
        elif nbr in seen:
            continue
        elif nbr == end:
            return 1
        else:
            seen.add(nbr)
            length = search(nbr, ignore_slopes)
            seen.discard(nbr)
            if length is not undefined and (longest is undefined or length > longest):
                longest = length
    return longest + 1 if longest is not undefined else longest


print(search(start))

# See 23.c
# print(search(start, True))
