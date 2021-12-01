from collections import deque
from patina import None_, Some
from lib.input import fetch_int_lines

data = fetch_int_lines()

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
