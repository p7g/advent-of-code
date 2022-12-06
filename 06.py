from aoc import *

buf = deque(data[:3], maxlen=4)
for i, c in enumerate(data[3:], 3):
    if len(set(buf)) == 4:
        break
    buf.append(c)
else:
    raise Exception("no marker")

print(i)

buf = deque(data[:13], maxlen=14)
for i, c in enumerate(data[13:], 13):
    if len(set(buf)) == 14:
        break
    buf.append(c)
else:
    raise Exception("no marker")

print(i)
