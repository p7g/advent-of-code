from lib.input import fetch_lines
from math import ceil

if __name__ == "__main__":
    min_time, times = fetch_lines()
    min_time = int(min_time)

    min_, t = float("inf"), None
    for time in times.split(","):
        if time == "x":
            continue
        time = int(time)
        ntimes = ceil(min_time / time)
        tt = ntimes * time
        if tt < min_:
            min_ = tt
            t = time

    print(t * (min_ - min_time))
