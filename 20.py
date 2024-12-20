import networkx as nx

from aoc import *

grid = data.splitlines()
dims = wh(grid)
G = nx.Graph()

for pt, c in pts(grid):
    if c in ".SE":
        G.add_node(pt)
        for nbr in pt.nbrs4(dims):
            if nbr.get(grid) in ".SE":
                G.add_edge(pt, nbr)
    if c == "S":
        START = pt
    elif c == "E":
        END = pt

base_time = nx.shortest_path_length(G, START, END)
path_pts = [tuple(pt) for pt, c in pts(grid) if c != "#"]
shortest_path_length = cache(nx.shortest_path_length)


def pt_pairs():
    for (ax, ay), (bx, by) in product(path_pts, repeat=2):
        d = abs(ax - bx) + abs(ay - by)
        if d <= 20:
            yield (ax, ay), (bx, by), d


s = s2 = 0
for A, B, d in pt_pairs():
    dtotal = (
        shortest_path_length(G, START, A)
        + d
        + shortest_path_length(G, B, END)
    )
    if dtotal >= base_time:
        continue
    saved_time = base_time - dtotal
    if saved_time >= 100:
        s += d == 2
        s2 += 1

print(s)
print(s2)
