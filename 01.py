from aoc import *

s = 0
for line in data.splitlines():
    digits = [int(c) for c in line if c.isdigit()]
    s += digits[0] * 10 + digits[-1]

print(s)


def find_digits(text):
    for i in range(len(text)):
        if text[i].isdigit():
            yield int(text[i])

        rest = text[i:]
        if rest.startswith("one"):
            yield 1
        elif rest.startswith("two"):
            yield 2
        elif rest.startswith("three"):
            yield 3
        elif rest.startswith("four"):
            yield 4
        elif rest.startswith("five"):
            yield 5
        elif rest.startswith("six"):
            yield 6
        elif rest.startswith("seven"):
            yield 7
        elif rest.startswith("eight"):
            yield 8
        elif rest.startswith("nine"):
            yield 9


s = 0
for line in data.splitlines():
    ds = list(find_digits(line))
    s += ds[0] * 10 + ds[-1]

print(s)
