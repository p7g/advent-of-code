from aoc import *
import networkx as nx

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)
G = nx.grid_2d_graph(w, h)

for y in range(h):
    for x in range(w):
        c = grid[y][x]
        if c == ".":
            G.remove_node((x, y))
        elif c == "F":
            G.remove_edges_from([
                ((x, y), (x - 1, y)),
                ((x, y), (x, y - 1)),
            ])
        elif c == "J":
            G.remove_edges_from([
                ((x, y), (x + 1, y)),
                ((x, y), (x, y + 1)),
            ])
        elif c == "L":
            G.remove_edges_from([
                ((x, y), (x - 1, y)),
                ((x, y), (x, y + 1)),
            ])
        elif c == "7":
            G.remove_edges_from([
                ((x, y), (x + 1, y)),
                ((x, y), (x, y - 1)),
            ])
        elif c == "-":
            G.remove_edges_from([
                ((x, y), (x, y - 1)),
                ((x, y), (x, y + 1)),
            ])
        elif c == "|":
            G.remove_edges_from([
                ((x, y), (x - 1, y)),
                ((x, y), (x + 1, y)),
            ])
        elif c == "S":
            source = x, y

cycle = nx.find_cycle(G, source)
num_steps = len(cycle)
print(num_steps // 2)


(ax, ay), (bx, by) = cycle[0]
dx, dy = bx - ax, by - ay
(ax, ay), (bx, by) = cycle[-1]
dx2, dy2 = bx - ax, by - ay
source_type = {
    ((0, 1), (0, 1)): "|",
    ((0, 1), (0, -1)): "|",
    ((0, -1), (0, 1)): "|",
    ((0, -1), (0, -1)): "|",
    ((1, 0), (1, 0)): "-",
    ((1, 0), (-1, 0)): "-",
    ((-1, 0), (1, 0)): "-",
    ((-1, 0), (-1, 0)): "-",
    ((0, -1), (1, 0)): "7",
    ((-1, 0), (0, -1)): "7",
    ((0, 1), (1, 0)): "J",
    ((1, 0), (0, 1)): "J",
    ((0, -1), (-1, 0)): "L",
    ((-1, 0), (0, 1)): "L",
    ((0, 1), (-1, 0)): "F",
    ((1, 0), (0, -1)): "F",
}[(dx, dy), (dx2, dy2)]

nodes = [source] + [n for _, n in cycle]
node_set = set(nodes)
G.remove_nodes_from(node for node in list(G.nodes) if node not in node_set)

area = set()
for y in range(h):
    inside = False
    on_pipe = None
    for x in range(w):
        c = grid[y][x]
        if c == "S":
            c = source_type

        if c in "|" and (x, y) in G.nodes:
            inside = not inside
        elif c == "-" and (x, y) in G.nodes:
            assert on_pipe
        elif c in "FL" and (x, y) in G.nodes:
            on_pipe = c
        elif c in "7J" and (x, y) in G.nodes:
            assert on_pipe
            if (on_pipe, c) in {("F", "J"), ("L", "7")}:
                inside = not inside
            on_pipe = None
        elif inside:
            area.add((x, y))

to_box = {
    "-": "─",
    "|": "│",
    "7": "┐",
    "J": "┘",
    "F": "┌",
    "L": "└",
}

for y2 in range(h):
    for x2 in range(w):
        if (x2, y2) in area:
            c = "I"
        elif (x2, y2) in G.nodes:
            c = grid[y2][x2]
            if c == "S":
                c = source_type
            c = to_box[c]
        else:
            c = "."
        print(c, end="")
    print()
print()

print(len(area))
