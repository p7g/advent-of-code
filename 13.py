from aoc import *

pairs = [
    (eval((ls := pair.splitlines())[0]), eval(ls[1])) for pair in data.split("\n\n")
]

def cmp(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        return -1 if left < right else 1
    elif isinstance(left, int):
        return cmp([left], right)
    elif isinstance(right, int):
        return cmp(left, [right])

    for l, r in zip_longest(left, right):
        if l is None:
            return -1
        elif r is None:
            return 1

        o = cmp(l, r)
        if o != 0:
            return o

    return 0

print(sum(i for i, p in enumerate(pairs, 1) if cmp(*p) == 1))

packets = [eval(l) for l in data.splitlines() if l]
packets.append([[2]])
packets.append([[6]])

decoder_key = 1
for i, p in enumerate(sorted(packets, key=cmp_to_key(cmp)), 1):
    if p in ([[6]], [[2]]):
        decoder_key *= i

print(decoder_key)
