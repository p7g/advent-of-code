from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()
    instructions = [(l[0], int(l[1:])) for l in data]
    delta = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}
    x, y = 0, 0
    wx, wy = 10, 1

    for action, value in instructions:
        if action in ("R", "L"):
            value //= 90
        if action == "L":
            value = 4 - value

        if action in ("R", "L"):
            dx, dy = wx - x, wy - y
            for _ in range(value):
                dx, dy = dy, -dx
            wx, wy = x + dx, y + dy
        elif action in ("N", "S", "E", "W"):
            dx, dy = delta[action]
            wx += dx * value
            wy += dy * value
        elif action == "F":
            dx, dy = (wx - x) * value, (wy - y) * value
            x += dx
            y += dy
            wx += dx
            wy += dy

    print(abs(x) + abs(y))
