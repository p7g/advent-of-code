from aoc import *

machines_raw = data.split("\n\n")
machines = []
for machine_raw in machines_raw:
    a, b, p = machine_raw.splitlines()
    A = Pt(*map(int, map(itemgetter(slice(1, None)), a.split(": ", 1)[1].split(", ", 1))))
    B = Pt(*map(int, map(itemgetter(slice(1, None)), b.split(": ", 1)[1].split(", ", 1))))
    prize = Pt(*map(int, map(itemgetter(slice(2, None)), p.split(": ", 1)[1].split(", ", 1))))
    machines.append((A, B, prize))

for offset in (0, 10000000000000):
    cost = 0
    for A, B, prize in machines:
        eq1 = (offset + prize.x) * A.y, A.x * A.y, B.x * A.y
        eq2 = (offset + prize.y) * A.x, A.y * A.x, B.y * A.x

        eq3 = eq1[0] - eq2[0], eq1[1] - eq2[1], eq1[2] - eq2[2]
        assert eq3[1] == 0
        b_presses, remainder = divmod(eq3[0], eq3[2])
        if remainder != 0:
            continue
        a_presses, remainder = divmod((offset + prize.x - (B.x * b_presses)), A.x)
        if remainder != 0:
            continue
        cost += 3 * a_presses + b_presses

    print(cost)
