from aoc import *

start, *lines = data.splitlines()
s = Counter([start.index("S")])
split = 0
for line in lines:
    news = Counter()
    for i, c in enumerate(line):
        if i not in s:
            continue
        elif c == "^":
            news[i - 1] += s[i]
            news[i + 1] += s[i]
            split += 1
        elif c == ".":
            news[i] += s[i]
    s = news
print(split)
print(s.total())
