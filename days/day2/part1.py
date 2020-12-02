from collections import Counter
from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines(2)
    num = 0

    for line in data:
        policy, pw = map(str.strip, line.split(":"))
        char_times = Counter(pw)
        times, c = policy.split(" ")
        min, max = map(int, times.split("-"))
        if min <= char_times[c] <= max:
            num += 1

    print(num)
