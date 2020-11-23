import numpy as np
from itertools import product
from os import path
from .day8lib import parse


def decode_image(image):
    w, h, d = image.shape
    result = np.empty((w, h), dtype=np.uint8, order="F")

    for x, y in product(range(w), range(h)):
        col = image[x, y, ...]
        for z in range(d):
            if col[z] != 2:
                result[x, y] = col[z]
                break
        else:
            result[x, y] = 2

    return result


chars = ["/", "@", " "]


def print_image(image):
    w, h = image.shape

    for y in range(h):
        for x in range(w):
            print(chars[image[x, y]], end="")
        print()


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        data = f.read().strip()

    layers = parse(data)
    print_image(decode_image(layers))
