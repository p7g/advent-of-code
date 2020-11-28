from lib.input import get_input
from lib.intcode import IntCodeVM


if __name__ == "__main__":
    data = get_input()
    vm = IntCodeVM.from_str(data)
    g = vm.run()
    next(g)

    north, south, west, east = range(1, 5)
    reverse = [0, south, north, east, west]
    dx = [0, 0, 0, -1, 1]
    dy = [0, 1, -1, 0, 0]
    hit_wall, moved_step, at_oxygen = range(3)
    G = {(0, 0): moved_step}
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
            if (x1, y1) not in G:
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
            G[x, y] = status
            if not backtrack:
                history.append(move)
        else:
            G[x + dx[move], y + dy[move]] = status

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
    for x, y in G.keys():
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y

    buf = ""
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if (x, y) not in G:
                buf += "/"
            elif G[x, y] == hit_wall:
                buf += "@"
            elif (x, y) == oxygen:
                buf += "O"
            elif (x, y) == (0, 0):
                buf += "X"
            else:
                buf += " "
        buf += "\n"
    print(buf)
    print(len(history))
