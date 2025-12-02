from aoc import *

ranges = [tuple(map(int, r.split("-", 1))) for r in data.split(",")]

s = 0
for first, last in ranges:
    for i in range(first, last + 1):
        si = str(i)
        if len(si) % 2 != 0:
            continue
        a, b = si[:len(si)//2], si[len(si)//2:]
        if a == b:
            s += i
print(s)

R = re.compile(r"^(?P<g>\d+?)(?P=g)+$")
s = 0
for first, last in ranges:
    for i in range(first, last + 1):
        if R.match(str(i)):
            s += i
print(s)
