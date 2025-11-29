#!/usr/bin/env python3

import dataclasses
import operator as op
import os
import re
import string
import sys
import typing as t
from bisect import bisect_left, bisect_right, insort
from collections import ChainMap, Counter, defaultdict, deque, namedtuple
from collections.abc import MutableSequence, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import cache, cmp_to_key, partial, reduce, total_ordering
from heapq import heapify, heappop, heappush, heappushpop, heapreplace
from itertools import (
    chain,
    combinations,
    count,
    cycle,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    zip_longest,
)
from math import (
    ceil,
    cos,
    cosh,
    dist,
    floor,
    gcd,
    hypot,
    lcm,
    log10,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
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

import more_itertools as it
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
from patina import Err, None_, Ok, Option, Result, Some
from pyrsistent import freeze, pbag, pdeque, pmap, pset, pvector, thaw

if t.TYPE_CHECKING:
    import datetime as dt

    import networkx as nx


data: str

__all__ = [
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
    "bisect_left",
    "bisect_right",
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
    "deepcopy",
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
    "groupby",
    "heapify",
    "heappop",
    "heappush",
    "heappushpop",
    "heapreplace",
    "hypot",
    "insort",
    "intersperse",
    "islice",
    "it",
    "itemgetter",
    "iterate",
    "last",
    "lcm",
    "log10",
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


def wh(grid: Sequence[Sequence[t.Any]]) -> Pt:
    return Pt(len(grid[0]), len(grid))


def grid_2d_graph_diag(w: int, h: int) -> nx.Graph:
    import networkx as nx

    G = nx.grid_2d_graph(w, h)
    G.add_edges_from(
        [((x, y), (x + 1, y + 1)) for x in range(w - 1) for y in range(h - 1)]
        + [((x + 1, y), (x, y + 1)) for x in range(w - 1) for y in range(h - 1)]
    )

    return G


def pts[T](grid: Sequence[Sequence[T]]) -> t.Iterator[tuple[Pt, T]]:
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

    def __rmul__(self, n: int) -> Pt:
        return self * n

    def __mod__(self, other: Pt) -> Pt:
        return Pt(self.x % other.x, self.y % other.y)

    def __rmatmul__[T](self, grid: Sequence[Sequence[T]]) -> T:
        return self.get(grid)

    def get[T](self, grid: Sequence[Sequence[T]]) -> T:
        return grid[self.y][self.x]

    def set[T](self, grid: Sequence[MutableSequence[T]], val: T) -> None:
        grid[self.y][self.x] = val

    def inbound(self, bound: tuple[int, int]) -> bool:
        x, y = self
        return 0 <= x < bound[0] and 0 <= y < bound[1]

    def nbrs4(self, bound: tuple[int, int] | None = None) -> t.Iterator[Pt]:
        for p in [self + (-1, 0), self + (0, 1), self + (1, 0), self + (0, -1)]:
            if bound and not p.inbound(bound):
                continue
            yield p

    def nbrs8(self, bound: tuple[int, int] | None = None) -> t.Iterator[Pt]:
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == dy == 0:
                continue
            p = self + (dx, dy)
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
    import runpy

    date = _get_challenge_date()
    script_path = _challenge_script_name(date)
    runpy.run_path(script_path)


def _challenge_script_name(date: dt.date) -> str:
    from pathlib import Path

    return str(Path(__file__).parent / f"{date.day:02}.py")


def _read_session() -> str:
    with open(".aoc-session") as f:
        return f.read().strip()


def _get_challenge_date() -> dt.date:
    import os
    from datetime import datetime
    from zoneinfo import ZoneInfo

    today = datetime.now(tz=ZoneInfo("America/New_York")).date()
    day = today.day

    try:
        if "AOC_DAY" in os.environ:
            day = int(os.environ["AOC_DAY"])
        elif __name__ != "__main__":
            day = int(sys.argv[0].split(".", 1)[0])
    except ValueError:
        pass

    year = int(os.environ.get("AOC_YEAR", today.year))
    return dt.date(year=year, month=12, day=day)


def _fetch_input_cached(date: dt.date) -> str:
    try:
        with open(_input_cache_path(date)) as f:
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
        timeout=10,
    )
    req.raise_for_status()
    return req.content.decode("ascii")


def _cache_input(date: dt.date, aoc_input: str) -> None:
    with open(_input_cache_path(date), "w") as f:
        f.write(aoc_input)


if __name__ == "__main__":
    _main()
