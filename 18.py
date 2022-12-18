from aoc import *
import networkx as nx

pts = {tuple(map(int, p.split(","))) for p in data.splitlines()}
G = nx.Graph()

for (x, y, z) in pts:
	G.add_node((x, y, z))
	for nbr in [
		(x + 1, y, z),
		(x - 1, y, z),
		(x, y + 1, z),
		(x, y - 1, z),
		(x, y, z + 1),
		(x, y, z - 1),
	]:
		if nbr in pts:
			G.add_edge((x, y, z), nbr)

area = 0
for node in G.nodes:
	assert G.degree[node] <= 6
	area += 6 - G.degree[node]

print(area)

maxx = maxy = maxz = 0
for (x, y, z) in pts:
	if x > maxx:
		maxx = x
	if y > maxy:
		maxy = y
	if z > maxz:
		maxz = z

G = nx.grid_graph((maxz + 1, maxy + 1, maxx + 1), periodic=True)

for x, y, z in pts:
	G.nodes[x, y, z]["lava"] = True

G.remove_nodes_from(n for n, attrs in list(G.nodes.items()) if attrs.get("lava"))

components = list(nx.connected_components(G))
biggest_component = max(components, key=len)
components.remove(biggest_component)

for component in components:
	for node in component:
		area -= 6 - G.degree[node]

print(area)
