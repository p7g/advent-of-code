from lib.input import fetch_lines
from .day5lib import get_id

if __name__ == "__main__":
    data = fetch_lines()
    print(max(map(get_id, data)))
