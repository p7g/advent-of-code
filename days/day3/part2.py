from lib.input import fetch_lines

if __name__ == "__main__":
    data = [l.strip() for l in fetch_lines(3)]
    prod = 1

    for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        x, y = 0, 0
        ntrees = 0
        while y < len(data):
            x += dx
            y += dy
            if data[y % len(data)][x % len(data[0])] == "#":
                ntrees += 1
        prod *= ntrees

    print(prod)
