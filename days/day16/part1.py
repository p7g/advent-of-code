from lib.input import get_input
from .day16lib import do_phases

if __name__ == "__main__":
    data = list(map(int, get_input().strip()))

    print("".join(map(str, do_phases(data, 100)[:8])))
