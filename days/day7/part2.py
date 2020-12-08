import networkx as nx
from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()
    G = nx.DiGraph()

    for rule in data:
        adj, col, _, _, *contains = rule.strip().split(" ")
        if len(contains) == 3:  # no other bags.
            continue
        container = f"{adj} {col}"
        G.add_node(container)
        contains = list(contains)
        contains.reverse()
        while contains:
            n, node = int(contains.pop()), contains.pop() + " " + contains.pop()
            contains.pop()
            G.add_edge(container, node, amount=n)

    def count_bags(node):
        n = 1
        for nbr in G[node]:
            n += G.edges[node, nbr]["amount"] * count(nbr)
        return n

    print(count_bags("shiny gold"))
