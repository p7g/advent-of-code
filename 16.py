import networkx as nx

from aoc import *

grid = data.splitlines()
dims = wh(grid)

D = {
    Pt(1, 0): "EAST",
    Pt(0, 1): "SOUTH",
    Pt(-1, 0): "WEST",
    Pt(0, -1): "NORTH",
}

G = nx.DiGraph()
for pt, c in pts(grid):
    if c == "#":
        continue
    elif c == "S":
        START = pt
    elif c == "E":
        END = pt

    assert c in "SE."

    nodes = [(pt, direction) for direction in D.values()]
    G.add_nodes_from(nodes)
    G.add_edges_from(
        (a, b, {"weight": 1000}) for a, b in product(nodes, repeat=2) if a != b
    )

    for nbr in pt.nbrs4(dims):
        if grid @ nbr == "#":
            continue
        direction = D[nbr - pt]
        G.add_edge((pt, direction), (nbr, direction), weight=1)

print(
    min(
        nx.shortest_path_length(G, (START, "EAST"), (END, direction), weight="weight")
        for direction in D.values()
    )
)

good_seats = set()
for direction in D.values():
    for path in nx.all_shortest_paths(G, (START, "EAST"), (END, direction), weight="weight"):
        good_seats.update(pt for pt, direction in path)
print(len(good_seats))
