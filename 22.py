from aoc import *

buyers = [int(n) for n in data.splitlines()]


def sequence(n):
    while True:
        yield n
        n ^= n * 64
        n %= 16777216
        n ^= n // 32
        n %= 16777216
        n ^= n * 2048
        n %= 16777216


print(sum(it.nth(sequence(b), 2000) for b in buyers))


def price_sequence(buyer):
    for n in sequence(buyer):
        yield n % 10


c = Counter()
for buyer in buyers:
    seq = deque(maxlen=4)
    seen = set()
    for prev_price, price in pairwise(islice(price_sequence(buyer), 0, 2000)):
        d = price - prev_price
        seq.append(d)
        if len(seq) < 4:
            continue
        k = tuple(seq)
        if k in seen:
            continue
        seen.add(k)
        c[k] += price

print(c.most_common(1)[0][1])
