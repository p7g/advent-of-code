from aoc import *

instructions = []
for line in data.splitlines():
    direction, distance, colour = line.split()
    instructions.append((direction, int(distance), int(colour.removeprefix("(#").removesuffix(")"), 16)))

directions = {"R": Pt(1, 0), "L": Pt(-1, 0), "U": Pt(0, -1), "D": Pt(0, 1)}

coords = [Pt(0, 0)]
for direction, distance, colour in instructions:
    coords.append(coords[-1] + directions[direction] * distance)

circumference = sum(abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in pairwise(coords))
area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in pairwise(coords)) // 2
print(area + 1 - circumference // 2 + circumference)

coords = [Pt(0, 0)]
for direction, distance, colour in instructions:
    direction = ["R", "D", "L", "U"][colour & 0xf]
    distance = colour >> 4
    coords.append(coords[-1] + directions[direction] * distance)

circumference = sum(abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in pairwise(coords))
area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in pairwise(coords)) // 2
print(area + 1 - circumference // 2 + circumference)
