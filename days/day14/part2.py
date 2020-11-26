from math import ceil
from os.path import join, dirname
from .day14lib import parse_input, build_graph


def amount_needed(G, node, n_fuel=1):
    if node == "FUEL":
        return n_fuel
    needed = 0
    for _, product in G.out_edges(node):
        needs_n = G.edges[node, product]["amount"]
        makes_n = G.nodes[product]["amount"]
        product_needed = amount_needed(G, product, n_fuel)
        needed += needs_n * ceil(product_needed / makes_n)
    return needed


if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    class Break(Exception):
        pass

    rules = parse_input(data)
    G = build_graph(rules)

    n = 1
    try:
        for step_size in (100000, 10000, 1000, 100, 10, 1):
            while True:
                needed = amount_needed(G, "ORE", n)
                if needed > 1_000_000_000_000:
                    if step_size == 1:
                        print(n - 1)
                        raise Break
                    n = n - step_size
                    break
                n += step_size
    except Break:
        pass
