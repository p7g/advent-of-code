from aoc import *

s = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

s2 = defaultdict(int, {
    "AX": 3,
    "BY": 3,
    "CZ": 3,
    "AY": 6,
    "BZ": 6,
    "CX": 6,
})

print(sum(s[b] + s2[a + b] for a, b in map(methodcaller("split", " "), data.splitlines())))

win = dict(zip("ABC", "YZX"))
tie = dict(zip("ABC", "XYZ"))
loss = dict(zip("ABC", "ZXY"))
s3 = dict(zip("XYZ", [loss, tie, win]))
s4 = dict(zip("XYZ", [0, 3, 6]))

print(sum(s[s3[b][a]] + s4[b] for a, b in map(methodcaller("split", " "), data.splitlines())))
