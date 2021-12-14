from aoc import *

tmpl, rules = data.split("\n\n")
rules = rules.splitlines()

rules = dict(tuple(r.split(" -> ")) for r in rules)

current = tmpl
for step in count(1):
    new = ""
    for l, r in it.pairwise(current):
        ins = rules.get(l + r, None)
        new += l
        if ins:
            new += ins
    new += r
    current = new

    if step == 10:
        break

c = Counter(current)
(_, most_common), *_, (_, least_common) = c.most_common(None)
print(most_common - least_common)


s_pairs = defaultdict(int)
for p in it.pairwise(tmpl):
    s_pairs[p] += 1

for step in count(1):
    new = defaultdict(int)
    for (l, r), c in s_pairs.items():
        ins = rules.get(l + r, None)
        if ins:
            new[l + ins] += c
            new[ins + r] += c
        else:
            new[l + r] += c
    s_pairs = new

    if step == 40:
        break


c = Counter()
for (l, r), count in s_pairs.items():
    c[l] += count

c[tmpl[-1]] += 1

(m, most_common), *_, (l, least_common) = c.most_common(None)
print(most_common - least_common)
