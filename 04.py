from aoc import *

possible_xmases = defaultdict(list)
Xmas = namedtuple("Xmas", "remaining_letters,direction")

num_xmas = 0
for y, line in enumerate(data.splitlines()):
    for x, letter in enumerate(line):
        if letter in ("X", "S"):
            remaining_letters = "MAS" if letter == "X" else "AMX"
            possible_xmases[x + 1, y].append(
                Xmas(peekable(iter(remaining_letters)), "right")
            )
            possible_xmases[x, y + 1].append(
                Xmas(peekable(iter(remaining_letters)), "down")
            )
            possible_xmases[x + 1, y + 1].append(
                Xmas(peekable(iter(remaining_letters)), "down right")
            )
            possible_xmases[x - 1, y + 1].append(
                Xmas(peekable(iter(remaining_letters)), "down left")
            )

        if pending_xmases := possible_xmases.pop((x, y), None):
            for pending_xmas in pending_xmases:
                if pending_xmas.remaining_letters.peek() == letter:
                    next(pending_xmas.remaining_letters)
                    try:
                        pending_xmas.remaining_letters.peek()
                    except StopIteration:
                        num_xmas += 1
                        continue
                    if pending_xmas.direction == "right":
                        next_pt = x + 1, y
                    elif pending_xmas.direction == "down":
                        next_pt = x, y + 1
                    elif pending_xmas.direction == "down right":
                        next_pt = x + 1, y + 1
                    elif pending_xmas.direction == "down left":
                        next_pt = x - 1, y + 1
                    possible_xmases[next_pt].append(pending_xmas)

print(num_xmas)

possible_xmases = defaultdict(list)
Xmas = namedtuple("Xmas", "remaining_letters,direction,a_pt")

c = Counter()
for y, line in enumerate(data.splitlines()):
    for x, letter in enumerate(line):
        if letter in ("M", "S"):
            remaining_letters = "AS" if letter == "M" else "AM"
            possible_xmases[x + 1, y + 1].append(
                Xmas(peekable(iter(remaining_letters)), "down right", None)
            )
            possible_xmases[x - 1, y + 1].append(
                Xmas(peekable(iter(remaining_letters)), "down left", None)
            )

        if pending_xmases := possible_xmases.pop((x, y), None):
            for pending_xmas in pending_xmases:
                if pending_xmas.remaining_letters.peek() == letter:
                    if letter == "A":
                        pending_xmas = pending_xmas._replace(a_pt=(x, y))
                    next(pending_xmas.remaining_letters)
                    try:
                        pending_xmas.remaining_letters.peek()
                    except StopIteration:
                        c[pending_xmas.a_pt] += 1
                        continue
                    if pending_xmas.direction == "down right":
                        next_pt = x + 1, y + 1
                    elif pending_xmas.direction == "down left":
                        next_pt = x - 1, y + 1
                    possible_xmases[next_pt].append(pending_xmas)

print(sum(n == 2 for _, n in c.most_common()))
