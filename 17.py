from aoc import *

grid = [list(map(int, line)) for line in data.splitlines()]
w, h = wh(grid)


def solve(a, b):
    start = (Pt(-1, 0), "d", 0)
    goal = Pt(w - 1, h - 1)
    prev = {}
    dist = defaultdict(lambda: float("inf"), {start: -1})
    Q = [
        [float("inf"), False, Pt(x, y), d, n]
        for x, y in product(range(w), range(h))
        for d in "lrud"
        for n in range(a, b)
    ]
    Q.append([-1, False, *start])
    heapify(Q)
    m = {tuple(e[2:]): e for e in Q}
    delta = {"r": Pt(1, 0), "l": Pt(-1, 0), "u": Pt(0, -1), "d": Pt(0, 1)}
    opposite = {"r": "l", "l": "r", "u": "d", "d": "u"}

    while Q:
        _dist, removed, u, d, n = heappop(Q)
        del m[u, d, n]
        if removed:
            continue
        elif u == goal:
            path = deque([u])
            while (u, d, n) in prev:
                u2 = prev[u, d, n][0]
                c = u
                diff = (u2 - u).unit()
                while c != u2:
                    c += diff
                    path.appendleft(c)
                u, d, n = prev[u, d, n]
            return sum(grid[y][x] for x, y in list(path)[2:])

        for direction in "lrud":
            if direction == d:
                nbr = (u + delta[direction], direction, n + 1)
            else:
                nbr = (u + delta[direction] * a, direction, a)

            if not nbr[0].inbound((w, h)) or nbr not in m:
                continue
            elif opposite[d] == direction:
                continue

            cost = sum(
                grid[y][x]
                for x, y in product(
                    range(min(u.x + 1, nbr[0].x), max(u.x, nbr[0].x + 1)),
                    range(min(u.y + 1, nbr[0].y), max(u.y, nbr[0].y + 1)),
                )
            )

            alt = dist[u, d, n] + cost
            if alt < dist[nbr]:
                prev[nbr] = u, d, n
                dist[nbr] = alt
                m[nbr][1] = True
                entry = [alt, False, *nbr]
                heappush(Q, entry)
                m[nbr] = entry
    else:
        raise Exception("no solution")


print(solve(1, 4))
print(solve(4, 11))
