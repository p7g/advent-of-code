from aoc import *
import networkx as nx

G = nx.Graph()

for line in data.splitlines():
    a, b = line.split("-")
    G.add_edge(a, b)


def find_paths(G, so_far, visited, from_="start"):
    edges = G[from_]

    for node in edges:
        if node == "end":
            yield [*so_far, "end"]
        elif node.islower() and node in visited:
            continue
        else:
            yield from find_paths(G, [*so_far, node], {*visited, node}, from_=node)


print(len(list(find_paths(G, ["start"], {"start"}))))


def find_paths(G, so_far, visited, from_="start", twice=False):
    edges = G[from_]

    for node in edges:
        if node == "start":
            continue
        elif node == "end":
            yield [*so_far, "end"]
        elif node.islower() and node in visited and twice:
            continue
        else:
            yield from find_paths(
                G,
                [*so_far, node],
                {*visited, node},
                from_=node,
                twice=twice or (node.islower() and node in visited),
            )


print(len(list(find_paths(G, ["start"], {}))))
