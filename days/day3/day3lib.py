import enum
from dataclasses import dataclass


class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Step:
    direction: Direction
    amount: int


def parse(raw_path):
    for s in raw_path.strip().split(","):
        yield Step(Direction(s[0]), int(s[1:]))


def all_points(steps):
    x, y = 0, 0

    for step in steps:
        for _ in range(step.amount):
            if step.direction is Direction.UP:
                y += 1
            elif step.direction is Direction.DOWN:
                y -= 1
            elif step.direction is Direction.RIGHT:
                x += 1
            elif step.direction is Direction.LEFT:
                x -= 1
            yield x, y


def manhattan_dist(p):
    return sum(map(abs, p))
