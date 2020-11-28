import networkx as nx
from lib.input import get_input
from lib.intcode import IntCodeVM


if __name__ == "__main__":
    data = get_input()
    vm = IntCodeVM.from_str(data)
    g = vm.run()
    next(g)

    directions = list(range(5))
    _, north, south, west, east = directions
    reverse = [0, south, north, east, west]
    dx = [0, 0, 0, -1, 1]
    dy = [0, 1, -1, 0, 0]
    hit_wall, moved_step, at_oxygen = range(3)
    coords = {(0, 0): moved_step}
    move = north
    x, y = 0, 0
    history = []
    backtrack = False

    def find_direction():
        neighbours = [
            (x - 1, y, west),
            (x + 1, y, east),
            (x, y - 1, south),
            (x, y + 1, north),
        ]
        for x1, y1, direction in neighbours:
            if (x1, y1) not in coords:
                return direction
        return None

    while True:
        if backtrack:
            move = reverse[history.pop()]
        status = g.send(move)
        next(g)
        if backtrack or status in (moved_step, at_oxygen):
            assert status in (moved_step, at_oxygen)
            x += dx[move]
            y += dy[move]
            coords[x, y] = status
            if not backtrack:
                history.append(move)
        else:
            coords[x + dx[move], y + dy[move]] = status

        if not history:
            backtrack = False

        move_ = find_direction()
        if move_ is None:
            if history:
                backtrack = True
            else:
                move = move % 4 + 1
        else:
            backtrack = False
            move = move_

        if status == at_oxygen:
            oxygen = x, y
            break

    xmin = xmax = 0
    ymin = ymax = 0
    for x, y in coords.keys():
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y

    w, h = (xmax - xmin) + 1, (ymax - ymin) + 1
    G = nx.grid_2d_graph(w, h)
    for (x, y), type_ in coords.items():
        node = x - xmin, y - ymin
        if type_ != hit_wall:
            G.add_node(node, visited=True)
            if type_ == at_oxygen:
                oxygen = node
        else:
            G.remove_node(node)

    to_visit = []
    for node in G:
        if not G.nodes[node].get("visited") and nx.has_path(G, oxygen, node):
            to_visit.append(node)

    delta_to_dir = dict(zip(zip(dx, dy), directions))
    x, y = oxygen
    while to_visit:
        to_visit = list(filter(lambda n: nx.has_path(G, (x, y), n), to_visit))
        # Always go to the closest one first so we don't try to move through
        # one (it could be a wall)
        to_visit.sort(key=lambda n: nx.shortest_path_length(G, (x, y), n), reverse=True)
        dest = to_visit.pop()
        if dest not in G:
            continue
        if not nx.has_path(G, (x, y), dest):
            G.remove_node(dest)
            continue
        for x1, y1 in nx.shortest_path(G, (x, y), dest)[1:]:
            direction = delta_to_dir[x1 - x, y1 - y]
            status = g.send(direction)
            next(g)
            if status == hit_wall:
                G.remove_node((x + dx[direction], y + dy[direction]))
                break
            else:
                G.add_node((x, y), visited=True)
                x += dx[direction]
                y += dy[direction]

    G.remove_nodes_from([n for n in G if not G.nodes[n].get("visited")])

    t = 0
    with_oxygen = {oxygen}
    while not all(n in with_oxygen for n in G):
        t += 1
        with_oxygen.update(
            {n for o in with_oxygen for n in G[o] if n not in with_oxygen}
        )

    buf = ""
    for y in range(h):
        for x in range(w):
            if (x, y) not in G:
                buf += "@"
            elif (x, y) == oxygen:
                buf += "O"
            elif (x, y) == (-xmin, -ymin):
                buf += "X"
            elif (x, y) in with_oxygen:
                buf += "~"
            elif not G.nodes[x, y].get("visited"):
                buf += "/"
            else:
                buf += " "
        buf += "\n"
    print(buf)
    print(t)
