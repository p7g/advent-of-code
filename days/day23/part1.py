from itertools import count
from lib.input import fetch

if __name__ == "__main__":
    data = fetch().strip()
    all_cups = list(map(int, data))
    cups = all_cups.copy()
    current = cups[0]

    for move in count():
        picked_up = [cups.pop((cups.index(current) + 1) % len(cups)) for _ in range(3)]
        dest = current - 1
        if dest < min(all_cups):
            dest = max(all_cups)
        while dest in picked_up:
            dest -= 1
            if dest < min(all_cups):
                dest = max(all_cups)
        idx = cups.index(dest)
        for i, c in enumerate(picked_up):
            cups.insert(idx + i + 1, c)
        current = cups[(cups.index(current) + 1) % len(cups)]
        if move == 99:
            break

    one_idx = cups.index(1)
    for i in range(len(cups) - 1):
        print(cups[(one_idx + i + 1) % len(cups)], end="")
    print()
