from os import path
from patina import Option
from .day3lib import all_points, parse, manhattan_dist


def find_closest(wires):
    a, b = map(set, map(all_points, map(parse, wires)))
    intersections = a & b

    closest = Option.None_()
    for dist in map(manhattan_dist, intersections):
        if closest.is_some() and dist > closest.unwrap():
            continue
        closest.replace(dist)

    return closest.unwrap()


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        print(find_closest(f.readlines()))
