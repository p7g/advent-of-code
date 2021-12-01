from aoc import *

data = list(map(int, data.splitlines()))

prev = None_()
inc = 0

for n in data:
    match prev:
        case Some(p) if n > p:
            inc += 1
    prev.replace(n)

print(inc)


prevsum = None_()
prevs = deque(data[:3], maxlen=3)
inc = 0

for i in data[3:]:
    newsum = sum(prevs)
    match prevsum:
        case Some(p) if newsum > p:
            inc += 1
    prevsum.replace(newsum)
    prevs.append(i)

newsum = sum(prevs)
match prevsum:
    case Some(p) if newsum > p:
        inc += 1

print(inc)
