from lib.input import fetch_lines
from functools import reduce
from operator import mul

if __name__ == "__main__":
    times = fetch_lines().split(",")

    eqns = [(-rem, int(mod)) for rem, mod in enumerate(times) if mod != "x"]
    M = reduce(mul, (mod for _, mod in eqns))

    x = 0
    for a, m in eqns:
        y = M // m
        z = pow(y, -1, m)
        x += a * y * z

    print(x % M)
