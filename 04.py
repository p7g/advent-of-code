from aoc import *

print(
    sum(
        1
        for (a, b), (x, y) in (
            (map(int, s.split("-")) for s in ss)
            for ss in (s.split(",") for s in data.splitlines())
        )
        if (aa := set(range(a, b + 1))) >= (xx := set(range(x, y + 1))) or xx > aa
    )
)

print(
    sum(
        1
        for (a, b), (x, y) in (
            (map(int, s.split("-")) for s in ss)
            for ss in (s.split(",") for s in data.splitlines())
        )
        if set(range(a, b + 1)) & set(range(x, y + 1))
    )
)
