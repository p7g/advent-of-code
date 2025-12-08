import networkx as nx

from aoc import *

coords = [tuple(map(int, line.split(",", 2))) for line in data.splitlines()]
ordered_connections = iter(
    sorted(
        it.distinct_combinations(coords, 2),
        key=lambda p: sqrt(sum((b - a) ** 2 for a, b in zip(*p))),
    )
)
G = nx.Graph(islice(ordered_connections, 0, 1000))
G.add_nodes_from(coords)
components = sorted(nx.connected_components(G), key=len, reverse=True)
print(reduce(mul, map(len, components[:3])))

for a, b in ordered_connections:
    G.add_edge(a, b)
    if nx.is_connected(G):
        print(a[0] * b[0])
        break
else:
    print("no solution")
