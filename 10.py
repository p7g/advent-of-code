from aoc import *


def int_from_bools(bools: Sequence[bool]) -> int:
    n = 0
    for b in reversed(bools):
        n <<= 1
        n |= b
    return n


machines = []
for line in data.splitlines():
    lights, *buttons, joltage = line.split()
    lights = int_from_bools([c == "#" for c in lights[1:-1]])
    buttons = [tuple(map(int, group[1:-1].split(","))) for group in buttons]
    joltage = tuple(map(int, joltage[1:-1].split(",")))
    machines.append((lights, buttons, joltage))


def match_lights(goal: int, buttons: tuple[int, ...]) -> int:
    states = {0}

    buttons = [
        int_from_bools([i in button for i in range(max(button) + 1)])
        for button in buttons
    ]

    for npresses in count(1):
        new_states = set()
        for lights in states:
            for button in buttons:
                new_lights = lights ^ button
                if new_lights == goal:
                    return npresses
                new_states.add(new_lights)
        states = new_states
    raise Exception("No solution")


s = 0
for goal, buttons, _joltage in machines:
    s += match_lights(goal, buttons)
print(s)


s = 0
for _lights, buttons, joltage in machines:
    A = [[0] * len(buttons) for _ in range(len(joltage))]
    for i in range(len(joltage)):
        for j in range(len(buttons)):
            A[i][j] = Fraction(int(i in buttons[j]))

    for row, j in zip(A, joltage):
        row.append(j)

    # forward elimination from wikipedia
    n, m = len(A[0]), len(A)
    n -= 1
    h = k = 0
    while h < m and k < n:
        i_max = max(range(h, m), key=lambda i: abs(A[i][k]))
        if A[i_max][k] == 0:
            k += 1  # No pivot in this column, pass to next column
            continue
        A[h], A[i_max] = A[i_max], A[h]
        for i in range(h + 1, m):
            f = A[i][k] / A[h][k]
            A[i][k] = 0
            for j in range(k + 1, n + 1):
                A[i][j] = A[i][j] - A[h][j] * f
        h += 1
        k += 1

    pivots = [None] * m
    for i in range(m):
        for j in range(n):
            if A[i][j] != 0:
                pivots[i] = j
                break

    # back substitution from chatgpt to get reduced row echelon form
    for pi, pj in reversed(list(enumerate(pivots))):
        if pj is None:
            continue

        # Normalize pivot to 1
        pivot = A[pi][pj]
        if pivot != 1:
            for j in range(pj, n + 1):
                A[pi][j] /= pivot

        # Make each column zero above the pivot
        for i in range(pi):
            f = A[i][pj]
            if f != 0:
                for j in range(pj, n + 1):
                    A[i][j] -= f * A[pi][j]

    # any columns without pivot are free
    free = [j for j in range(n) if j not in pivots]

    # no free variables, only one solution
    if not free:
        x = [0] * n
        for i in range(m):
            pj = pivots[i]
            if pj is None:
                continue
            x[pj] = A[i][n]
        s += sum(x)
        continue

    # find bounds of free variables
    max_per_free = {}
    for fcol in free:
        affected = buttons[fcol]
        if affected:
            max_per_free[fcol] = min(joltage[i] for i in affected)
        else:
            max_per_free[fcol] = 0

    ranges = [range(max_per_free[col] + 1) for col in free]

    # brute force free variables to find least sum
    least = None
    for free_vals in product(*ranges):
        x = [0] * n

        for idx, col in enumerate(free):
            x[col] = free_vals[idx]

        ok = True
        for i in range(m):
            pj = pivots[i]
            if pj is None:
                if A[i][n] != 0:
                    ok = False
                    break
                continue

            rhs = A[i][n]
            val = rhs
            for j in free:
                val -= A[i][j] * x[j]

            if val < 0:
                ok = False
                break

            x[pj] = val

        if not ok:
            continue

        if all(xi >= 0 and xi.is_integer() for xi in x):
            total = sum(x)
            if least is None or total < least:
                least = total

    assert least is not None
    s += least

print(s)
