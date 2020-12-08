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

    n = 0
    for node in G.nodes:
        if node == "shiny gold":
            continue
        if nx.has_path(G, node, "shiny gold"):
            n += 1
    print(n)
