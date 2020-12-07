from lib.input import fetch

if __name__ == "__main__":
    data = fetch(6)

    groups = data.strip().split("\n\n")

    sum_ = 0
    for group in groups:
        seen = set()
        for person in group.strip().splitlines():
            seen |= set(person)
        sum_ += len(seen)

    print(sum_)
