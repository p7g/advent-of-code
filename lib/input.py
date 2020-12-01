import inspect
from pathlib import Path


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
