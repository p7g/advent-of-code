from aoc import *

points, instructions = data.split("\n\n")

points = {tuple(map(int, p.split(","))) for p in points.splitlines()}
original_points = points.copy()

instructions = [
    ((s := i.lstrip("fold along ").split("="))[0], int(s[1]))
    for i in instructions.splitlines()
]

for axis, pos in instructions:
    new_points = set()

    for px, py in points:
        if axis == "y":
            new_points.add((px, pos - abs(py - pos)))
        elif axis == "x":
            new_points.add((pos - abs(px - pos), py))

    points = new_points
    break

print(len(points))

points = original_points.copy()

for axis, pos in instructions:
    new_points = set()

    for px, py in points:
        if axis == "y":
            new_points.add((px, pos - abs(py - pos)))
        elif axis == "x":
            new_points.add((pos - abs(px - pos), py))

    points = new_points


max_x = max_y = float("-inf")


for x, y in points:
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y


g = [
    ["." for _ in range(max_x + 1)]
    for _ in range(max_y + 1)
]


for x, y in points:
    g[y][x] = "#"

print("\n".join("".join(l) for l in g))
