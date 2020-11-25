from collections import defaultdict
from os.path import dirname, join
from lib.intcode import IntCodeVM

if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    grid = defaultdict(lambda: 0)
    vm = IntCodeVM.from_str(data).run()

    try:
        while True:
            x = next(vm)
            y = next(vm)
            grid[x, y] = next(vm)
    except StopIteration:
        pass

    print(len([v for v in grid.values() if v == 2]))
