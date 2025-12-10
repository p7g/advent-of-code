from aoc import *

coords = [Pt(*map(int, l.split(",", 1))) for l in data.splitlines()]


def area(a: Pt, b: Pt) -> int:
    dx, dy = b - a
    return (abs(dy) + 1) * (abs(dx) + 1)


print(max(area(a, b) for a, b in it.distinct_combinations(coords, 2)))


# https://old.reddit.com/r/adventofcode/comments/1phywvn/comment/nt2hps9/
# https://old.reddit.com/r/adventofcode/comments/1phywvn/comment/nt6ku4l/
boxes = sorted(
    it.distinct_combinations(coords, 2), key=lambda p: area(*p), reverse=True
)
for a, b in boxes:
    x1, x2 = minmax(a.x, b.x)
    y1, y2 = minmax(a.y, b.y)
    for c, d in pairwise(coords + coords[:1]):
        if not (
            y2 <= min(c.y, d.y)
            or y1 >= max(c.y, d.y)
            or x2 <= min(c.x, d.x)
            or x1 >= max(c.x, d.x)
        ):
            break
    else:
        break

print(area(a, b))
