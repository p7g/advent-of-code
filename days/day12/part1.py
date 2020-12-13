from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()
    instructions = [(l[0], int(l[1:])) for l in data]
    delta = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}

    directions = ["E", "S", "W", "N"]
    x, y = 0, 0
    direction = 0

    for action, value in instructions:
        if action in ("R", "L"):
            value //= 90
        if action == "L":
            value = -value

        if action in ("R", "L"):
            direction += value
            direction %= len(directions)
        elif action in ("N", "S", "E", "W"):
            dx, dy = delta[action]
            for _ in range(value):
                x += dx
                y += dy
        elif action == "F":
            dx, dy = delta[directions[direction]]
            for _ in range(value):
                x += dx
                y += dy

    print(abs(x) + abs(y))
