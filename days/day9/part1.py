from itertools import combinations
from lib.input import fetch_int_lines

if __name__ == "__main__":
    data = fetch_int_lines()

    preamble = data[:25]
    for i, n in enumerate(data[25:]):
        for a, b in combinations(data[i : i + 25], 2):
            if a + b == n:
                break
        else:
            print(n)
            break
