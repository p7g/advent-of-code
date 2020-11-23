import networkx as nx
from os import path
from .day6lib import graph_from_input


def number_of_transfers(g):
    # Number of edges minus 2
    return len(nx.shortest_path(g, "YOU", "SAN")) - 3


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        raw = f.read()
    g = graph_from_input(raw)
    print(number_of_transfers(g))
