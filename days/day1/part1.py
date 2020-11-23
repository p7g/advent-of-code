import numpy as np
from os import path
from .day1lib import fuel_req


if __name__ == "__main__":
    print(
        fuel_req(
            np.loadtxt(path.join(path.dirname(__file__), "input.txt"), dtype=np.int64)
        ).sum()
    )
