import os
from os.path import dirname, join
from patina import Option
from lib.intcode import IntCodeVM

if __name__ == "__main__":
    with open(join(dirname(__file__), "input.txt"), "r") as f:
        data = f.read()

    do_print = bool(os.getenv("AOC_PRINT"))
    score = 0
    vm = IntCodeVM.from_str(data)
    vm.memory[0] = 2
    gen = vm.run()
    ball_x = Option.None_()
    paddle_x = Option.None_()
    paddle_dir = None
    grid = {}

    try:
        while True:
            x = gen.send(paddle_dir)
            if x is None:
                x = gen.send(paddle_dir)
            y = gen.send(paddle_dir)
            z = gen.send(paddle_dir)
            ball_dx = 0
            if (x, y) != (-1, 0):
                grid[x, y] = z
            if x == -1 and y == 0:
                score = z
            elif z == 4:
                ball_x.replace(x)
            elif z == 3:
                paddle_x.replace(x)

            d = ball_x.zip(paddle_x).map(lambda xs: xs[0] - xs[1]).unwrap_or(0)
            if d < 0:
                paddle_dir = -1
            elif d > 0:
                paddle_dir = 1
            else:
                paddle_dir = 0

            if do_print:
                import time
                import numpy as np

                xs, ys = [], []
                for x, y in grid.keys():
                    xs.append(x)
                    ys.append(y)

                xmax, ymax = max(xs), max(ys)
                w, h = xmax + 1, ymax + 1
                board = np.zeros((w, h), dtype=np.uint8)
                for (x, y), block_type in grid.items():
                    board[x, h - y - 1] = block_type

                types = [" ", "#", "@", "=", "O"]
                print("\033[2J", end="")
                buf = [f"score: {score}"]
                for y in range(h):
                    inner_buf = []
                    for x in range(w):
                        inner_buf.append(types[board[x, h - y - 1]])
                    buf.append("".join(inner_buf))
                print("\n".join(buf))
                time.sleep(0.0001)
    except StopIteration:
        pass

    if not do_print:
        print(score)
