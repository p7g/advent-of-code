from aoc import *

# caveman
s = 0
for line in data.splitlines():
    s += max(
        int(line[i] + line[j])
        for i in range(len(line))
        for j in range(i + 1, len(line))
    )
print(s)

s = 0
for line in data.splitlines():
    # greedy:
    # track pos
    # find largest number with required remaining digits after
    n = ""
    pos = 0
    for i in range(12):
        m = None
        for j in range(pos, len(line) - (11 - i)):
            if m is None or line[j] > m[1]:
                m = j, line[j]
        pos, nn = m
        pos += 1
        n += nn
    s += int(n)
print(s)
