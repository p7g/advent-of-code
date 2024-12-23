import networkx as nx

from aoc import *

G = nx.Graph(tuple(line.split("-", 1)) for line in data.splitlines())

s = 0
for nodes in nx.enumerate_all_cliques(G):
    if len(nodes) != 3:
        continue
    s += any(n[0] == "t" for n in nodes)

print(s)
print(",".join(sorted(nodes)))
