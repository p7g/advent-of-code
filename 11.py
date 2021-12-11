from aoc import *

octopi = [list(map(int, l)) for l in data.splitlines()]
nflashes = 0

for tick in count(1):
    flashed = set()
    to_flash = []
    for y, row in enumerate(octopi):
        for x, col in enumerate(row):
            octopi[y][x] += 1
            if octopi[y][x] > 9:
                to_flash.append((x, y))

    while to_flash:
        x, y = to_flash.pop()
        if (x, y) in flashed:
            continue
        flashed.add((x, y))
        for nbr in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]:
            if nbr in flashed:
                continue
            nx, ny = nbr
            if nx < 0 or nx >= len(octopi[0]) or ny < 0 or ny >= len(octopi):
                continue
            octopi[ny][nx] += 1
            if octopi[ny][nx] > 9:
                to_flash.append(nbr)

    nflashes += len(flashed)
    for x, y in flashed:
        octopi[y][x] = 0

    if tick == 100:
        break

print(nflashes)

octopi = [list(map(int, l)) for l in data.splitlines()]

for tick in count(1):
    flashed = set()
    to_flash = []
    for y, row in enumerate(octopi):
        for x, col in enumerate(row):
            octopi[y][x] += 1
            if octopi[y][x] > 9:
                to_flash.append((x, y))

    while to_flash:
        x, y = to_flash.pop()
        if (x, y) in flashed:
            continue
        flashed.add((x, y))
        for nbr in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]:
            if nbr in flashed:
                continue
            nx, ny = nbr
            if nx < 0 or nx >= len(octopi[0]) or ny < 0 or ny >= len(octopi):
                continue
            octopi[ny][nx] += 1
            if octopi[ny][nx] > 9:
                to_flash.append(nbr)

    for x, y in flashed:
        octopi[y][x] = 0

    if len(flashed) == len(octopi) * len(octopi[0]):
        break

print(tick)
