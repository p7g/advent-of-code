from aoc import *

reports = [[int(n) for n in line.split()] for line in data.splitlines()]


def safe(report):
    s = sign(report[1] - report[0])
    if s == 0:
        return False
    for a, b in pairwise(report):
        if 1 <= (b - a) * s <= 3:
            pass
        else:
            return False
    return True


print(sum(safe(r) for r in reports))


def safe2(report):
    if safe(report):
        return True
    for i in range(len(report)):
        report2 = report[:i] + report[i + 1:]
        if safe(report2):
            return True
    return False


print(sum(safe2(r) for r in reports))
