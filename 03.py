from aoc import *


def matchword(it, word):
    try:
        for i, c in enumerate(word):
            if it[i] != c:
                return False
    except (StopIteration, IndexError):
        return False
    else:
        for _ in range(len(word)):
            next(it)
        return True


part1 = 0
part2 = 0
it = peekable(iter(data))
enabled = True
while True:
    if matchword(it, "do()"):
        enabled = True
    elif matchword(it, "don't()"):
        enabled = False
    elif matchword(it, "mul"):
        if it.peek(None) != "(":
            continue
        next(it)
        digs = ""
        for i in range(3):
            c = it.peek(None)
            if not c or not c.isdigit():
                break
            digs += c
            next(it)
        if not digs:
            continue
        A = int(digs)
        if it.peek(None) != ",":
            continue
        next(it)
        digs = ""
        for i in range(3):
            c = it.peek(None)
            if not c or not c.isdigit():
                break
            digs += c
            next(it)
        if not digs:
            continue
        B = int(digs)
        if it.peek(None) != ")":
            continue
        next(it)
        part1 += A * B
        part2 += A * B * enabled
    elif next(it, None) is None:
        break

print(part1)
print(part2)
