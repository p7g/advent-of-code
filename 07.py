from aoc import *

root = {}
root[".."] = root

cwd = root
for line in data.splitlines():
    if line.startswith("$ "):
        cmd = line[2:]
        match cmd.split(" "):
            case ["cd", "/"]:
                cwd = root
            case ["cd", d]:
                cwd = cwd[d]
    else:
        x, name = line.split(" ", 1)
        if x == "dir":
            cwd[name] = {"..": cwd}
        else:
            cwd[name] = int(x)

solution = 0


def dirsz(dir_):
    tot = 0
    for name, x in dir_.items():
        if name == "..":
            continue
        if isinstance(x, int):
            tot += x
        else:
            tot += dirsz(x)
    if tot < 100_000:
        global solution
        solution += tot
    return tot


rootsz = dirsz(root)
print(solution)

reqd = 30_000_000 - (70_000_000 - rootsz)
min_ = float('inf')


def dirsz2(dir_):
    global min_
    tot = 0
    for name, x in dir_.items():
        if name == "..":
            continue
        if isinstance(x, int):
            tot += x
        else:
            tot += dirsz2(x)
    if tot >= reqd and tot < min_:
        min_ = tot
    return tot


dirsz2(root)
print(min_)
