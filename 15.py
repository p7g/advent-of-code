from aoc import *


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


print(sum(hash(s) for s in data.split(",")))

boxes = [{} for _ in range(256)]

for s in data.split(","):
    if "=" in s:
        label, f = s.split("=")
        box = boxes[hash(label)]
        box[label] = int(f)
    else:
        label = s.removesuffix("-")
        box = boxes[hash(label)]
        box.pop(label, None)

p = 0
for i, box in enumerate(boxes):
    for j, (label, f) in enumerate(box.items()):
        p += (i + 1) * (j + 1) * f
print(p)
