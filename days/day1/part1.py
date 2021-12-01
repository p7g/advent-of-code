from patina import None_, Some
from lib.input import fetch_int_lines

data = fetch_int_lines()

prev = None_()
inc = 0

for n in data:
    match prev:
        case Some(p) if n > p:
            inc += 1
    prev.replace(n)

print(inc)
