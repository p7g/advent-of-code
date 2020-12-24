from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()

    paths = []
    for line in data:
        steps = []
        while line:
            if line.startswith("ne"):
                steps.append("ne")
                line = line[2:]
            elif line.startswith("nw"):
                steps.append("nw")
                line = line[2:]
            elif line.startswith("se"):
                steps.append("se")
                line = line[2:]
            elif line.startswith("sw"):
                steps.append("sw")
                line = line[2:]
            else:
                steps.append(line[0])
                line = line[1:]
        paths.append(steps)

    flipped = set()

    delta = {
        "nw": (0, 1, -1),
        "ne": (1, 0, -1),
        "e": (1, -1, 0),
        "se": (0, -1, 1),
        "sw": (-1, 0, 1),
        "w": (-1, 1, 0),
    }

    for path in paths:
        x, y, z = 0, 0, 0
        for step in path:
            assert x + y + z == 0
            dx, dy, dz = delta[step]
            x += dx
            y += dy
            z += dz
        if (x, y, z) in flipped:
            flipped.remove((x, y, z))
        else:
            flipped.add((x, y, z))

    def nbrs(p):
        x, y, z = p
        yield x, y + 1, z - 1
        yield x + 1, y, z - 1
        yield x + 1, y - 1, z
        yield x, y - 1, z + 1
        yield x - 1, y, z + 1
        yield x - 1, y + 1, z

    def tiles():
        all_tiles = set()
        ts = list(flipped)
        for t in ts:
            all_tiles.add(t)
            all_tiles |= set(nbrs(t))
        return all_tiles

    for _ in range(100):
        new_state = flipped.copy()

        for t in tiles():
            nflippednbrs = sum(n in flipped for n in nbrs(t))
            if t in flipped:
                if nflippednbrs == 0 or nflippednbrs > 2:
                    new_state.remove(t)
            elif nflippednbrs == 2:
                new_state.add(t)

        flipped = new_state

    print(len(flipped))
