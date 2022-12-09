from aoc import *

add = lambda p1, p2: tuple(a + b for a, b in zip(p1, p2))
sub = lambda p1, p2: tuple(a - b for a, b in zip(p1, p2))

head = (0, 0)
tail = (0, 0)
seen_positions = {tail}

for direction, distance in [((ps := l.split(" ", 1))[0], int(ps[1])) for l in data.splitlines()]:
    match direction:
        case "R":
            dx, dy = 1, 0
        case "L":
            dx, dy = -1, 0
        case "U":
            dx, dy = 0, 1
        case "D":
            dx, dy = 0, -1
        case _:
            raise NotImplementedError

    for i in range(distance):
        head = add(head, (dx, dy))
        dx2, dy2 = sub(head, tail)
        if abs(dx2) <= 1 and abs(dy2) <= 1:
            continue
        tail = add(tail, (sign(dx2), sign(dy2)))
        seen_positions.add(tail)

print(len(seen_positions))


head = (0, 0)
tails = [(0, 0) for _ in range(9)]
seen_positions = {(0, 0)}

for direction, distance in [((ps := l.split(" ", 1))[0], int(ps[1])) for l in data.splitlines()]:
    match direction:
        case "R":
            dx, dy = 1, 0
        case "L":
            dx, dy = -1, 0
        case "U":
            dx, dy = 0, 1
        case "D":
            dx, dy = 0, -1
        case _:
            raise NotImplementedError

    for i in range(distance):
        head = add(head, (dx, dy))
        for i in range(len(tails)):
            tail = tails[i]
            dx2, dy2 = sub(head if i == 0 else tails[i - 1], tail)
            if abs(dx2) <= 1 and abs(dy2) <= 1:
                continue
            tails[i] = add(tail, (sign(dx2), sign(dy2)))
        seen_positions.add(tails[-1])

print(len(seen_positions))
