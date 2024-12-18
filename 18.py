import networkx as nx

from aoc import *

dims = Pt(71, 71)
nsimulate = 1024

start = 0, 0
end = tuple(dims - Pt(1, 1))
coords = [tuple(map(int, l.split(","))) for l in data.splitlines()]

G = nx.grid_2d_graph(*dims)
G.remove_nodes_from(coords[:nsimulate])

print(nx.shortest_path_length(G, start, end))

for c in coords[nsimulate:]:
	G.remove_node(c)
	if not nx.has_path(G, start, end):
		print(",".join(map(str, c)))
		break
