from aoc import *

ranges, ingredients = data.split("\n\n")
ranges = [tuple(map(int, range.split("-"))) for range in ranges.splitlines()]
ingredients = list(map(int, ingredients.splitlines()))

n = 0
for i in ingredients:
    for lo, hi in ranges:
        if lo <= i <= hi:
            n += 1
            break
print(n)


mergedranges = []
for lo, hi in sorted(ranges):
    if not mergedranges or lo > mergedranges[-1][1]:
        mergedranges.append((lo, hi))
    else:
        mergedranges[-1] = (mergedranges[-1][0], max(hi, mergedranges[-1][1]))

print(sum(hi - lo + 1 for lo, hi in mergedranges))
