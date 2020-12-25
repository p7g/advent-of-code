from itertools import count
from lib.input import fetch_int_lines

if __name__ == "__main__":
    pub_a, pub_b = fetch_int_lines()

    for i in count():
        if pow(7, i, 20201227) == pub_a:
            loop_a = i
            break

    print(pow(pub_b, loop_a, 20201227))
