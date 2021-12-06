from aoc import *


def unit(n):
    return -1 if n < 0 else 1


class Line(namedtuple("Line", "x1,y1,x2,y2")):
    def is_horizontal(self):
        x1, _y1, x2, _y2 = self
        return x1 == x2

    def is_vertical(self):
        _x1, y1, _x2, y2 = self
        return y1 == y2

    def points(self):
        x1, y1, x2, y2 = self
        dx = x2 - x1
        dy = y2 - y1
        yield from zip_longest(
            range(x1, x2 + unit(dx), unit(dx)) if dx else [],
            range(y1, y2 + unit(dy), unit(dy)) if dy else [],
            fillvalue=y1 if dx else x1,
        )


lines = []
for input_line in data.splitlines():
    from_pt, to_pt = input_line.split(" -> ")
    lines.append(Line(*map(int, chain(from_pt.split(","), to_pt.split(",")))))


straight_lines = [l for l in lines if l.is_horizontal() or l.is_vertical()]
nvents = Counter()

for line in straight_lines:
    for pt in line.points():
        nvents[pt] += 1

print(len([k for k, v in nvents.items() if v >= 2]))


nvents = Counter()

for line in lines:
    for pt in line.points():
        nvents[pt] += 1

print(len([k for k, v in nvents.items() if v >= 2]))
