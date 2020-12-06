from lib.input import fetch_lines
from .day5lib import get_id

if __name__ == "__main__":
    data = fetch_lines()
    ids = list(map(get_id, data))
    min_, max_ = min(ids), max(ids)
    ids = set(ids)

    for i in range(min_ + 1, max_ - 1):
        if i - 1 in ids and i + 1 in ids and i not in ids:
            print(i)
            break
