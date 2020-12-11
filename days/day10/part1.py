from collections import Counter
from lib.input import fetch_int_lines

if __name__ == "__main__":
    data = fetch_int_lines()
    data.sort()
    data.append(data[-1] + 3)

    diffs = Counter()
    joltage = 0

    for j in data:
        diffs[j - joltage] += 1
        joltage = j

    print(diffs[1] * diffs[3])
