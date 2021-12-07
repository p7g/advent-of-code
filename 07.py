from aoc import *

data = list(map(int, data.split(",")))

smallest = float('inf')
result_pos = None
for i in range(min(data), max(data) + 1):
    total_fuel = sum(abs(pos - i) for pos in data)
    if total_fuel < smallest:
        smallest = total_fuel
        result_pos = i

print(result_pos, smallest)


def fuel_cost(pos, dest):
    # I'm dumb so
    tot = 0
    for i in range(abs(pos - dest) + 1):
        tot += i
    return tot


smallest = float('inf')
result_pos = None
for i in range(min(data), max(data) + 1):
    total_fuel = sum(fuel_cost(pos, i) for pos in data)
    if total_fuel < smallest:
        smallest = total_fuel
        result_pos = i

print(result_pos, smallest)
