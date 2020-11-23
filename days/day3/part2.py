from os import path
from .day3lib import all_points, parse


def find_shortest(wires):
    a, b = map(set, map(all_points, map(parse, wires)))
    intersections = a & b

    def count_steps(wire, to_point):
        steps = 0
        for point in all_points(parse(wire)):
            steps += 1
            if point == to_point:
                return steps
        raise ValueError(f"{wire} doesn't reach {to_point}")

    a, b = wires
    return min(count_steps(a, p) + count_steps(b, p) for p in intersections)


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        print(find_shortest(f.readlines()))
