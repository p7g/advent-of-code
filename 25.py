from aoc import *
import networkx as nx

G = nx.Graph()

for line in data.splitlines():
    l, r = line.split(": ")
    G.add_edges_from((l, r2) for r2 in r.split())

cut = nx.minimum_edge_cut(G)
G.remove_edges_from(cut)
a, b = nx.connected_components(G)
print(len(a) * len(b))
