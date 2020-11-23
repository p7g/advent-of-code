import networkx as nx
from os import path
from .day6lib import graph_from_input


def number_of_orbits(g):
    total = 0
    for node in g.nodes:
        total += len(nx.shortest_path(g, node, "COM")) - 1
    return total


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        raw = f.read()
    g = graph_from_input(raw)
    print(number_of_orbits(g))
