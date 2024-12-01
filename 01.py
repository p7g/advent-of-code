from aoc import *

a, b = zip(*(map(int, line.split()) for line in data.splitlines()))

print(sum(abs(aa - bb) for aa, bb in zip(sorted(a), sorted(b))))

c = Counter(b)

print(sum(n * c[n] for n in a))
