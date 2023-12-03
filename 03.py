import networkx as nx

from aoc import *

lines = data.splitlines()
W, H = wh(lines)
G = grid_2d_graph_diag(W, H)


def complete_number(num_str: str, pos: tuple[int, int]) -> None:
    x, y = pos
    num = int(num_str)
    num_pos = (x - len(num_str), y)
    G.nodes[num_pos]["num"] = num
    remove_nodes = [(x2, y) for x2 in range(x - len(num_str) + 1, x)]
    G.add_edges_from(
        (num_pos, nbr) for node in remove_nodes for nbr in nx.neighbors(G, node)
    )
    G.remove_nodes_from(remove_nodes)


for y, line in enumerate(lines):
    num_str = ""
    x = 0

    for x, c in enumerate(line):
        if c.isdigit():
            num_str += c
        elif num_str:
            complete_number(num_str, (x, y))
            num_str = ""

        if c == "." or c.isdigit():
            continue
        else:
            G.nodes[x, y]["sym"] = c

    if num_str:
        complete_number(num_str, (x + 1, y))
        num_str = ""

s = 0
for x, y in G.nodes:
    if "sym" not in G.nodes[x, y]:
        continue

    for nbr in nx.neighbors(G, (x, y)):
        if "num" in G.nodes[nbr]:
            s += G.nodes[nbr]["num"]

print(s)

s = 0
for x, y in G.nodes:
    if G.nodes[x, y].get("sym") != "*":
        continue

    adjacent_nums = [
        G.nodes[nbr]["num"] for nbr in nx.neighbors(G, (x, y)) if "num" in G.nodes[nbr]
    ]
    if len(adjacent_nums) != 2:
        continue

    s += adjacent_nums[0] * adjacent_nums[1]

print(s)
