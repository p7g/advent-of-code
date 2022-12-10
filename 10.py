from aoc import *

X = 1
instrs = list(reversed(data.splitlines()))
in_progress = None_()
ss = 0

for cycle in count(1):
    if not instrs and not in_progress:
        break

    pos = (cycle - 1) % 40
    if pos in [X - 1, X, X + 1]:
        print("#", end="")
    else:
        print(".", end="")
    if pos == 39:
        print()

    if (cycle - 20) % 40 == 0:
        assert cycle <= 220
        ss += cycle * X

    match in_progress.take():
        case Some((op, arg)):
            assert op == "addx"
            X += arg
        case _:
            instr = instrs.pop()

            if instr == "noop":
                continue

            op, arg = instr.split(" ")
            assert op == "addx"
            in_progress.replace((op, int(arg)))

print(ss)
