import networkx as nx
from itertools import product

from lib.input import fetch_lines

if __name__ == "__main__":
    data = [list(l) for l in fetch_lines()]
    w, h = len(data[0]), len(data)

    def nbrs_diag(data, G, n):
        nbrs = []
        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            x, y = n
            if dx == 0 and dy == 0:
                continue
            x, y = x + dx, y + dy
            while True:
                if (x, y) not in G:
                    break
                if state(data, (x, y)) != ".":
                    nbrs.append((x, y))
                    break
                x, y = x + dx, y + dy
        return nbrs

    def state(data, n):
        x, y = n
        return data[y][x]

    def rule1(data, G, n):
        if state(data, n) == "L" and all(
            state(data, nbr) != "#" for nbr in nbrs_diag(data, G, n)
        ):
            return "#"
        return None

    def rule2(data, G, n):
        if (
            state(data, n) == "#"
            and len([nbr for nbr in nbrs_diag(data, G, n) if state(data, nbr) == "#"])
            >= 5
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
