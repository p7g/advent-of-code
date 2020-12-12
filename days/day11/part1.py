import networkx as nx
from itertools import product

from lib.input import fetch_lines

if __name__ == "__main__":
    data = [list(l) for l in fetch_lines()]
    w, h = len(data[0]), len(data)

    def nbrs_diag(G, n):
        x, y = n
        nbrs = list(G[n])
        for nbr in product([x - 1, x + 1], [y - 1, y + 1]):
            if nbr in G:
                nbrs.append(nbr)
        return nbrs

    def state(data, n):
        x, y = n
        return data[y][x]

    def rule1(data, G, n):
        if state(data, n) == "L" and all(
            state(data, nbr) != "#" for nbr in nbrs_diag(G, n)
        ):
            return "#"
        return None

    def rule2(data, G, n):
        if (
            state(data, n) == "#"
            and len([nbr for nbr in nbrs_diag(G, n) if state(data, nbr) == "#"]) >= 4
        ):
            return "L"
        return None

    def part1(G, data):
        new_data = [row.copy() for row in data]
        nchanged = 0
        for y in range(h):
            for x in range(w):
                new_state = rule1(data, G, (x, y)) or rule2(data, G, (x, y))
                if new_state:
                    new_data[y][x] = new_state
                    nchanged += 1
        if nchanged == 0:
            return new_data
        return part1(G, new_data)

    def count_occupied(data):
        return sum(c == "#" for row in data for c in row)

    G = nx.freeze(nx.grid_2d_graph(w, h))

    print(count_occupied(part1(G, data)))
