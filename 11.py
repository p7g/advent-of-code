from aoc import *

monkey_specs = data.split("\n\n")
monkeys = []

for spec in monkey_specs:
    lines = spec.splitlines()
    starting_items = [int(n) for n in lines[1].split(": ", 1)[-1].split(", ")]
    op = lines[2].split(": ", 1)[-1]
    test_divisor = int(lines[3].rsplit(" ", 1)[-1])
    dests = (
        int(lines[5].rsplit(" ", 1)[-1]),
        int(lines[4].rsplit(" ", 1)[-1]),
    )
    monkeys.append((starting_items, op, test_divisor, dests, [0]))

for i in count(1):
    for items, op, test_divisor, dests, n_inspections in monkeys:
        items_to_throw = list(items)
        items.clear()

        for item in items_to_throw:
            n_inspections[0] += 1
            env = {"old": item}
            exec(op, env, env)
            item = env["new"]
            item //= 3
            monkeys[dests[item % test_divisor == 0]][0].append(item)

    if i == 20:
        break

a, b = sorted([m[4][0] for m in monkeys], reverse=True)[:2]
print(a * b)

monkeys = []

for spec in monkey_specs:
    lines = spec.splitlines()
    starting_items = [int(n) for n in lines[1].split(": ", 1)[-1].split(", ")]
    op = lines[2].split(": ", 1)[-1]
    test_divisor = int(lines[3].rsplit(" ", 1)[-1])
    dests = (
        int(lines[5].rsplit(" ", 1)[-1]),
        int(lines[4].rsplit(" ", 1)[-1]),
    )
    monkeys.append((starting_items, op, test_divisor, dests, [0]))

mod = lcm(*(m[2] for m in monkeys))

for i in count(1):
    for items, op, test_divisor, dests, n_inspections in monkeys:
        items_to_throw = list(items)
        items.clear()

        for item in items_to_throw:
            n_inspections[0] += 1
            env = {"old": item}
            exec(op, env, env)
            item = env["new"]
            item %= mod
            monkeys[dests[item % test_divisor == 0]][0].append(item)

    if i == 10000:
        break

a, b = sorted([m[4][0] for m in monkeys], reverse=True)[:2]
print(a * b)
