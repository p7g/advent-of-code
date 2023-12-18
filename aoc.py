#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import os
import more_itertools as it
import operator as op
import re
import string
import sys
import typing as t
from collections import ChainMap, Counter, defaultdict, deque, namedtuple
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key, lru_cache, partial, reduce, total_ordering
from heapq import heapify, heappop, heappush, heappushpop, heapreplace
from itertools import (
    chain,
    combinations,
    count,
    cycle,
    islice,
    permutations,
    product,
    repeat,
    zip_longest,
)
from math import ceil, cos, cosh, floor, gcd, hypot, sin, sinh, sqrt, tan, tanh
from more_itertools import (
    chunked,
    first,
    flatten,
    intersperse,
    iterate,
    last,
    mark_ends,
    minmax,
    nth,
    one,
    padded,
    pairwise,
    partition,
    peekable,
    tail,
    take,
    triplewise,
    windowed,
)
from operator import (
    add,
    and_,
    attrgetter,
    floordiv,
    itemgetter,
    methodcaller,
    mod,
    mul,
    or_,
    sub,
    truediv,
    xor,
)
from patina import Err, None_, Ok, Option, Result, Some
from pyrsistent import freeze, pbag, pdeque, pmap, pset, pvector, thaw

if t.TYPE_CHECKING:
    import datetime as dt
    import networkx as nx

try:
    from math import dist
except ImportError:

    def dist(ns):
        raise NotImplementedError


try:
    from math import lcm
except ImportError:

    def lcm(*integers: t.SupportsIndex) -> int:
        return abs(reduce(op.mul, integers)) // gcd(*integers)


try:
    from functools import cache
except ImportError:

    def cache(fn):
        return lru_cache(None)(fn)


data: str

__all__ = [  # noqa
    "ChainMap",
    "Counter",
    "Enum",
    "Err",
    "None_",
    "Ok",
    "Option",
    "Pt",
    "Result",
    "Some",
    "add",
    "and_",
    "attrgetter",
    "cache",
    "ceil",
    "chain",
    "chunked",
    "cmp_to_key",
    "combinations",
    "cos",
    "cosh",
    "count",
    "cycle",
    "data",
    "dataclass",
    "dataclasses",
    "defaultdict",
    "deque",
    "dist",
    "first",
    "flatten",
    "floor",
    "floordiv",
    "freeze",
    "gcd",
    "grid_2d_graph_diag",
    "heapify",
    "heappop",
    "heappush",
    "heappushpop",
    "heapreplace",
    "hypot",
    "intersperse",
    "islice",
    "it",
    "itemgetter",
    "iterate",
    "last",
    "lcm",
    "mark_ends",
    "methodcaller",
    "minmax",
    "mod",
    "mul",
    "namedtuple",
    "nth",
    "one",
    "op",
    "or_",
    "os",
    "padded",
    "pairwise",
    "partial",
    "partition",
    "pbag",
    "pdeque",
    "peekable",
    "permutations",
    "pmap",
    "product",
    "pset",
    "pts",
    "pvector",
    "re",
    "reduce",
    "repeat",
    "sign",
    "sin",
    "sinh",
    "string",
    "sqrt",
    "sub",
    "sys",
    "t",
    "tail",
    "take",
    "tan",
    "tanh",
    "thaw",
    "total_ordering",
    "triplewise",
    "truediv",
    "wh",
    "windowed",
    "xor",
    "zip_longest",
]


def sign(n):
    if n == 0:
        return 0
    return 1 if n > 0 else -1


def wh(grid: Sequence[Sequence[t.Any]]) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def grid_2d_graph_diag(w: int, h: int) -> "nx.Graph":
    import networkx as nx

    G = nx.grid_2d_graph(w, h)
    G.add_edges_from(
        [((x, y), (x + 1, y + 1)) for x in range(w - 1) for y in range(h - 1)]
        + [((x + 1, y), (x, y + 1)) for x in range(w - 1) for y in range(h - 1)]
    )

    return G


T = t.TypeVar("T")


def pts(grid: Sequence[Sequence[T]]) -> t.Iterator[tuple["Pt", T]]:
    w, h = wh(grid)
    for y, x in product(range(h), range(w)):
        p = Pt(x, y)
        yield p, p.get(grid)


class Pt(t.NamedTuple):
    x: int
    y: int

    def __add__(self, b) -> Pt:
        if not isinstance(b, (Pt, tuple)):
            return NotImplemented
        (ax, ay), (bx, by) = self, b
        return Pt(ax + bx, ay + by)

    def __neg__(self) -> Pt:
        return Pt(-self.x, -self.y)

    def __sub__(self, b: Pt) -> Pt:
        return self + -b

    def __mul__(self, n: int) -> Pt:
        return Pt(self.x * n, self.y * n)

    def get(self, grid: Sequence[Sequence[T]]) -> T:
        return grid[self.y][self.x]

    def inbound(self, bound: tuple[int, int]) -> bool:
        x, y = self
        return 0 <= x < bound[0] and 0 <= y < bound[1]

    def nbrs4(self, bound: tuple[int, int] | None = None) -> t.Iterator[Pt]:
        for p in [self + (-1, 0), self + (0, 1), self + (1, 0), self + (0, -1)]:
            if bound and not p.inbound(bound):
                continue
            yield p

    def unit(self) -> Pt:
        return Pt(sign(self.x), sign(self.y))


def __getattr__(name: str) -> t.Any:
    if name == "data":
        return _fetch_input_cached(_get_challenge_date())
    else:
        raise AttributeError(name)


def _main() -> None:
    date = _get_challenge_date()
    script_path = _challenge_script_name(date)
    with open(script_path, "r") as f:
        script_src = f.read()
    code = compile(source=script_src, filename=script_path, mode="exec")
    exec(code, {}, {})


def _challenge_script_name(date: dt.date) -> str:
    from pathlib import Path

    return str(Path(__file__).parent / f"{date.day:02}.py")


def _read_session() -> str:
    with open(".aoc-session", "r") as f:
        return f.read().strip()


def _get_challenge_date() -> dt.date:
    import datetime as dt
    import os

    today = dt.date.today()

    day = int(os.environ.get("AOC_DAY", today.day))
    year = int(os.environ.get("AOC_YEAR", today.year))
    return dt.date(year=year, month=12, day=day)


def _fetch_input_cached(date: dt.date) -> str:
    try:
        with open(_input_cache_path(date), "r") as f:
            return f.read().strip("\r\n")
    except FileNotFoundError:
        pass
    input_data = _fetch_input(date)
    _cache_input(date, input_data)
    return input_data


def _input_cache_path(date: dt.date) -> str:
    from pathlib import Path

    cache_dir = Path(__file__).parent / ".aoc-cache"
    cache_dir.mkdir(exist_ok=True)

    return str(cache_dir / f"{date.year}-{date.day}.txt")


def _fetch_input(date: dt.date) -> str:
    import requests

    req = requests.get(
        f"https://adventofcode.com/{date.year}/day/{date.day}/input",
        cookies={"session": _read_session()},
    )
    req.raise_for_status()
    return req.content.decode("ascii")


def _cache_input(date: dt.date, aoc_input: str) -> None:
    with open(_input_cache_path(date), "w") as f:
        f.write(aoc_input)


if __name__ == "__main__":
    _main()
