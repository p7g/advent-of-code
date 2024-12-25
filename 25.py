from aoc import *

items = data.split("\n\n")

keys = []
locks = []

for item in items:
	lines = item.splitlines()
	H = len(lines)
	if all(c == "#" for c in lines[0]):
		pins = []
		for x in range(len(lines[0])):
			for y in range(len(lines)):
				if lines[y][x] == ".":
					break
			pins.append(y - 1)
		locks.append(pins)
	else:
		pins = []
		for x in range(len(lines[0])):
			for y in range(len(lines) - 1, -1, -1):
				if lines[y][x] == ".":
					break
			pins.append(5 - y)
		keys.append(pins)

match = 0
for lock, key in product(locks, keys):
	for a, b in zip(lock, key):
		if a + b + 2 > H:
			break
	else:
		match += 1
		continue
print(match)
