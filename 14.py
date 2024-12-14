from aoc import *

dims = Pt(101, 103)

vectors = []
for line in data.splitlines():
    p, v = (
        (b := a.split("=", 1)[1].split(",", 1)) and Pt(int(b[0]), int(b[1]))
        for a in line.split()
    )
    vectors.append((p, v))

q1 = q2 = q3 = q4 = 0
for p, v in vectors:
    x, y = (p + v * 100) % dims
    if x < dims.x // 2:
        if y < dims.y // 2:
            q1 += 1
        elif y >= ceil(dims.y / 2):
            q2 += 1
    elif x >= ceil(dims.x / 2):
        if y < dims.y // 2:
            q3 += 1
        elif y >= ceil(dims.y / 2):
            q4 += 1

print(q1 * q2 * q3 * q4)


g = [[0] * dims.x for _ in range(dims.y)]
for i in count():
    for y in range(dims.y):
        for x in range(dims.x):
            g[y][x] = 0

    for p, v in vectors:
        x, y = (p + v * i) % dims
        g[y][x] += 1

    if any(n > 1 for l in g for n in l):
        continue

    os.system("clear")
    print(i)
    for line in g:
        print("".join(str(n) if n else "." for n in line))
    input()
