from collections import defaultdict
from lib.intcode import IntCodeVM

# up, right, down, left
delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def painted_panels(code, tiles=None):
    tiles = tiles or defaultdict(lambda: 0)
    x, y = 0, 0
    direction = 0
    vm = IntCodeVM.from_str(code).run()

    try:
        while True:
            next(vm)
            tiles[x, y] = vm.send(tiles[x, y])
            turn = next(vm) or -1
            direction = (direction + turn) % 4
            dx, dy = delta[direction]
            x += dx
            y += dy
    except StopIteration:
        pass

    return tiles
