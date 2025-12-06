from aoc import *

s = 0
for *operands, opstr in zip(*(row.split() for row in data.splitlines())):
    s += reduce({"+": add, "*": mul}[opstr], map(int, operands))
print(s)


lines = data.splitlines()
p = s = 0
for i in range(len(lines[0])):
    if all(line[i] == " " for line in lines):
        continue
    elif lines[-1][i] != " ":
        s += p
        append, p = {"+": (add, 0), "*": (mul, 1)}[lines[-1][i]]

    d = "".join(c for j in range(len(lines) - 1) if (c := lines[j][i]) != " ")
    p = append(p, int(d))
s += p
print(s)
