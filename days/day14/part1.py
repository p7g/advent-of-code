from math import ceil
from os.path import join, dirname
from .day14lib import parse_input, build_graph


def amount_needed(G, node):
    if node == "FUEL":
        return 1
    needed = 0
    for _, product in G.out_edges(node):
        needs_n = G.edges[node, product]["amount"]
        makes_n = G.nodes[product]["amount"]
        product_needed = amount_needed(G, product)
        needed += needs_n * ceil(product_needed / makes_n)
    return needed


if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    rules = parse_input(data)
    G = build_graph(rules)
    print(amount_needed(G, "ORE"))
