from os import path
from patina import Option
from .day10lib import parse_points, points_between


def count_visible_asteroids(ps, a):
    pset = set(ps)
    total = 0
    for b in ps:
        if b == a:
            continue
        between = points_between(a, b)
        if any(p in pset for p in between):
            continue
        total += 1
    return total


def find_most_visibility(ps):
    best = Option.None_()
    for p in ps:
        visible = count_visible_asteroids(ps, p)
        if best.is_some() and best.unwrap()[0] > visible:
            continue
        best.replace((visible, p))
    return best.unwrap()


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    ps = parse_points(data)
    print(find_most_visibility(ps))
