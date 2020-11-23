import numpy as np

WIDTH, HEIGHT = 25, 6


def parse(data, width=WIDTH, height=HEIGHT):
    depth = len(data) // (width * height)
    return np.fromiter(map(int, data), dtype=np.uint8).reshape(
        width, height, depth, order="F"
    )


def layer(a, i):
    return a[..., i]


def flatten_layer(a):
    return a.reshape(WIDTH * HEIGHT)
