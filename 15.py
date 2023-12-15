from aoc import *
from unittest.mock import ANY


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


print(sum(hash(s) for s in data.split(",")))

boxes = [deque() for _ in range(256)]

for s in data.split(","):
    if "=" in s:
        label, f = s.split("=")
        box = boxes[hash(label)]
        try:
            box[box.index((label, ANY))] = (label, int(f))
        except ValueError:
            box.append((label, int(f)))
    else:
        label = s.removesuffix("-")
        box = boxes[hash(label)]
        try:
            box.remove((label, ANY))
        except ValueError:
            pass

p = 0
for i, box in enumerate(boxes):
    for j, (label, f) in enumerate(box):
        p += (i + 1) * (j + 1) * f
print(p)
