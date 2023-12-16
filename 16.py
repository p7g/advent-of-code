from aoc import *

grid = [list(line) for line in data.splitlines()]
w, h = wh(grid)
delta = {"r": (1, 0), "l": (-1, 0), "u": (0, -1), "d": (0, 1)}

def run(start):
    beams: set[tuple[int, int, str]] = {start}
    seen = set()
    energized = set()
    while beams:
        # print(beams)
        beam = beams.pop()
        x, y, d = beam

        p = Pt(x, y)
        while True:
            p += delta[d]
            if not p.inbound((w, h)):
                break
            energized.add(p)
            c = p.get(grid)
            if c == "." or (c == "-" and d in "lr") or (c == "|" and d in "ud"):
                continue
            break

        if not p.inbound((w, h)):
            continue
        elif (*p, d) in seen:
            continue

        seen.add((*p, d))
        if p.get(grid) == "/":
            beams.add((*p, {"r": "u", "d": "l", "l": "d", "u": "r"}[d]))
        elif p.get(grid) == "\\":
            beams.add((*p, {"r": "d", "d": "r", "l": "u", "u": "l"}[d]))
        elif p.get(grid) == "-":
            beams.add((*p, "r"))
            beams.add((*p, "l"))
        elif p.get(grid) == "|":
            beams.add((*p, "d"))
            beams.add((*p, "u"))
        else:
            raise NotImplementedError

    return len(energized)

print(run((-1, 0, "r")))

starts = (
    [(x, -1, "d") for x in range(w)]
    + [(x, h, "u") for x in range(w)]
    + [(-1, y, "r") for y in range(h)]
    + [(w, y, "l") for y in range(h)]
)

print(max(run(start) for start in starts))
