from aoc import *

rules, updates = data.split("\n\n")

edges = {tuple(map(int, rule.split("|", 1))) for rule in rules.splitlines()}

s = 0
out_of_order = []
for update in updates.splitlines():
    update = [int(n) for n in update.split(",")]

    update_iter = iter(update)
    n = next(update_iter)
    for page in update_iter:
        assert page != n
        if (n, page) not in edges:
            out_of_order.append(update)
            break
        n = page
    else:
        s += update[len(update) // 2]

print(s)

s2 = 0
for update in out_of_order:
    update = sorted(update, key=cmp_to_key(lambda a, b: -1 if (a, b) in edges else 1))
    s2 += update[len(update) // 2]

print(s2)
