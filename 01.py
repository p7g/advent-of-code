from aoc import *

max = None
current = 0
for line in data.splitlines():
    if line == "":
        if max is None or current > max:
            max = current
        current = 0
    else:
        current += int(line)


print(max)


print(sum(sorted((sum(map(int, e.splitlines())) for e in data.split("\n\n")), reverse=True)[:3]))
