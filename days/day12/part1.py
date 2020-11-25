from os.path import dirname, join
from .day12lib import parse_input, simulate


if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    moons = parse_input(data)
    print(simulate(moons, 1000))
