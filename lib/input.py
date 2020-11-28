import inspect
from os.path import join, dirname


def get_input():
    caller_file = inspect.currentframe().f_back.f_globals["__file__"]
    with open(join(dirname(caller_file), "input.txt"), "r") as f:
        return f.read()
