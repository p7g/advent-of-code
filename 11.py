from aoc import *

stones = Counter(int(n) for n in data.split())

for i in range(75):
    new_stones = Counter()
    for stone, n in stones.items():
        if stone == 0:
            new_stones[1] += n
        elif (ndigits := floor(log10(stone)) + 1) % 2 == 0:
            l, r = divmod(stone, 10 ** (ndigits // 2))
            new_stones[l] += n
            new_stones[r] += n
        else:
            new_stones[stone * 2024] += n
    stones = new_stones

    if i == 24:
        print(sum(stones.values()))

print(sum(stones.values()))
