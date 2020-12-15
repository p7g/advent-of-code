from lib.input import fetch_int_commasep
from .day15lib import go

if __name__ == "__main__":
    print(go(fetch_int_commasep(), 30_000_000))
