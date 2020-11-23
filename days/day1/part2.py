import numpy as np
from os import path
from .day1lib import fuel_req


def fuel_req_rec(mass):
    fuel = 0
    current = fuel_req(mass)
    while current > 0:
        fuel += current
        current = fuel_req(current)
    return fuel


if __name__ == "__main__":
    a = np.loadtxt(path.join(path.dirname(__file__), "input.txt"), dtype=np.int64)
    print(np.vectorize(fuel_req_rec)(a).sum())
