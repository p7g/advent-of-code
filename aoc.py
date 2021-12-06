#!/usr/bin/env python3

from __future__ import annotations

import datetime as dt
import os
import more_itertools as it
import networkx as nx
import numpy as np
import operator as op
import re
import sys
import typing as t
from collections import ChainMap, Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import partial, reduce
from itertools import chain, combinations, count, cycle, permutations, product, repeat, zip_longest
from math import ceil, cos, cosh, dist, floor, gcd, hypot, sin, sinh, tan, tanh
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


data: str

__all__ = [  # noqa
    "ChainMap",
    "Counter",
    "Enum",
    "Err",
    "None_",
    "Ok",
    "Option",
    "Result",
    "Some",
    "add",
    "and_",
    "attrgetter",
    "ceil",
    "chain",
    "combinations",
    "cos",
    "cosh",
    "count",
    "cycle",
    "data",
    "dataclass",
    "defaultdict",
    "deque",
    "dist",
    "floor",
    "floordiv",
    "gcd",
    "hypot",
    "it",
    "itemgetter",
    "methodcaller",
    "mod",
    "mul",
    "namedtuple",
    "np",
    "nx",
    "op",
    "or_",
    "os",
    "partial",
    "permutations",
    "product",
    "re",
    "reduce",
    "repeat",
    "sin",
    "sinh",
    "sub",
    "sys",
    "tan",
    "tanh",
    "truediv",
    "xor",
    "zip_longest",
]


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
            return f.read().strip()
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