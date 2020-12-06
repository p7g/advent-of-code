import inspect
import os
from meta import YEAR
from pathlib import Path

default_day = os.getenv("DAY")


def _get_input(nth_frame):
    frame = inspect.stack()[nth_frame]
    module = inspect.getmodule(frame[0])
    input_path = Path(module.__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def get_input(strip=True):
    content = _get_input(2)
    return content.strip() if strip else content


def get_input_lines(strip=True):
    lines = _get_input(2).splitlines()
    return [l.strip() for l in lines] if strip else lines


def fetch(day=default_day):
    import os
    import requests

    input_path = Path(__file__).parent.parent / "days" / f"day{day}" / "input.txt"
    if input_path.exists():
        with open(input_path, "r") as f:
            return f.read()

    r = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}/input",
        cookies={"session": os.environ["AOC_SESSION"]},
    )
    r.raise_for_status()
    content = r.content.decode("ascii")
    with open(input_path, "w") as f:
        f.write(content)
    return content


def fetch_lines(day=default_day):
    return fetch(day).strip().splitlines()


def fetch_int_lines(day=default_day):
    return list(map(int, fetch_lines(day)))


def fetch_commasep(day=default_day):
    return fetch(day).strip().split(",")


def fetch_int_commasep(day=default_day):
    return list(map(int, fetch_commasep(day)))
