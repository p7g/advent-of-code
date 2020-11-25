import numpy as np
from collections import defaultdict
from os.path import dirname, join
from .day11lib import painted_panels


if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        code = f.read()

    tiles = defaultdict(lambda: 0)
    tiles[0, 0] = 1
    tiles = painted_panels(code, tiles)

    xs, ys = [], []
    for x, y in tiles.keys():
        xs.append(x)
        ys.append(y)

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    w, h = xmax - xmin, ymax - ymin
    dx, dy = xmin, ymin

    board = np.zeros((w + 1, h + 1), dtype=np.uint8)
    for (x, y), colour in tiles.items():
        x -= dx
        y -= dy
        board[x, h - y] = colour

    for y in range(h + 1):
        for x in range(w):
            print("#" if board[x, y] else " ", end="")
        print()
