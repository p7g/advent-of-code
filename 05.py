from aoc import *

raw_initial_state, raw_steps = data.split("\n\n", 1)

steps = []
for raw_step in raw_steps.splitlines():
    _, quantity, _, source, _, dest = raw_step.split(" ")
    steps.append(tuple(map(int, [quantity, source, dest])))

state = None
for row in reversed(raw_initial_state.splitlines()[:-1]):
    ncols = (len(row) + 1) // 4
    if state is None:
        state = tuple([] for _ in range(ncols))
    for i, colno in enumerate(range(ncols)):
        if (c := row[colno * 4 + 1]) != " ":
            state[i].append(c)

assert state is not None

for qty, src, dst in steps:
    for _ in range(qty):
        state[dst - 1].append(state[src - 1].pop())

print("".join([col[-1] if col else " " for col in state]))


state = None
for row in reversed(raw_initial_state.splitlines()[:-1]):
    ncols = (len(row) + 1) // 4
    if state is None:
        state = tuple([] for _ in range(ncols))
    for i, colno in enumerate(range(ncols)):
        if (c := row[colno * 4 + 1]) != " ":
            state[i].append(c)

assert state is not None

for qty, src, dst in steps:
    state[dst - 1].extend(reversed([state[src - 1].pop() for _ in range(qty)]))

print("".join([col[-1] if col else " " for col in state]))
