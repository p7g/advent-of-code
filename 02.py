from aoc import *


data = [(l.split(" ")[0], int(l.split(" ")[1])) for l in data.splitlines()]

depth = 0
horizontal_pos = 0

for direction, amount in data:
    if direction == "forward":
        horizontal_pos += amount
    elif direction == "down":
        depth += amount
    elif direction == "up":
        depth -= amount


print(depth * horizontal_pos)


depth = 0
horizontal_pos = 0
aim = 0

for direction, amount in data:
    if direction == "down":
        aim += amount
    elif direction == "up":
        aim -= amount
    elif direction == "forward":
        horizontal_pos += amount
        depth += aim * amount

print(depth * horizontal_pos)
