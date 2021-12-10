from aoc import *

mapping = {"(": ")", "{": "}", "[": "]", "<": ">"}

opening = set(mapping.keys())
closing = set(mapping.values())

pts = 0

for line in data.splitlines():
    stack = []
    for c in line:
        if c in opening:
            stack.append(c)
        elif c in closing:
            if c != mapping[stack.pop()]:
                pts += {")": 3, "]": 57, "}": 1197, ">": 25137}[c]
                break


print(pts)


non_corrupt = []
for line in data.splitlines():
    stack = []
    for c in line:
        if c in opening:
            stack.append(c)
        elif c in closing:
            if c != mapping[stack.pop()]:
                break
    else:
        non_corrupt.append(line)


scores = []
for line in non_corrupt:
    stack = []
    for c in line:
        if c in opening:
            stack.append(c)
        elif c in closing:
            if c != mapping[stack.pop()]:
                break

    if stack:
        score = 0
        completion = [mapping[c] for c in reversed(stack)]
        for c in completion:
            score *= 5
            score += {")": 1, "]": 2, "}": 3, ">": 4}[c]
        scores.append(score)

print(sorted(scores)[len(scores) // 2])
