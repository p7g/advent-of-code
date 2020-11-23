import numpy as np
from operator import itemgetter
from os import path
from .day8lib import parse, layer, flatten_layer

if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        data = f.read().strip()

    image = parse(data)
    i, _n = max(enumerate(np.count_nonzero(image, (0, 1))), key=itemgetter(1))
    counts = np.bincount(flatten_layer(layer(image, i)))

    print(counts[1] * counts[2])
