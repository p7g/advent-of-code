from os import path
from .day11lib import painted_panels


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = f.read()

    print(len(painted_panels(code)))
