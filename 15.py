from aoc import *
import networkx as nx


risk_map = [list(map(int, l)) for l in data.splitlines()]

G = nx.grid_2d_graph(len(risk_map), len(risk_map[0]), create_using=nx.DiGraph())

for _, (x, y), attrs in G.edges.data():
    attrs["risk"] = risk_map[y][x]

d, p = nx.single_source_dijkstra(
    G, (0, 0), (len(risk_map[0]) - 1, len(risk_map) - 1), weight="risk"
)
print(d)


def copy_inc(dest, offset, source, inc_by):
    ox, oy = offset
    for y in range(oy, oy + len(source)):
        for x in range(ox, ox + len(source[0])):
            dest[y][x] = source[y - oy][x - ox] + inc_by
            if dest[y][x] > 9:
                dest[y][x] %= 9


h, w = len(risk_map), len(risk_map[0])
assert h == w
big_map = [[0] * (w * 5) for _ in range(h * 5)]
copy_inc(big_map, (0, 0), risk_map, 0)

for y_offset in range(0, h * 5, h):
    for x_offset in range(0, w * 5, w):
        if y_offset == x_offset == 0:
            continue
        copy_inc(big_map, (x_offset, y_offset), risk_map, (y_offset + x_offset) // w)

G = nx.grid_2d_graph(len(big_map), len(big_map[0]), create_using=nx.DiGraph())

for _, (x, y), attrs in G.edges.data():
    attrs["risk"] = big_map[y][x]

d, p = nx.single_source_dijkstra(
    G, (0, 0), (len(big_map[0]) - 1, len(big_map) - 1), weight="risk"
)
print(d)
