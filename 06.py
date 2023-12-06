from aoc import *

times_raw, distances_raw = data.splitlines()
times = [int(t) for t in times_raw.split()[1:]]
distances = [int(d) for d in distances_raw.split()[1:]]
races = list(zip(times, distances, strict=True))


def roots(a, b, c):
    return (
        (-b + sqrt(b**2 - 4 * a *c)) / 2 * a,
        (-b - sqrt(b**2 - 4 * a *c)) / 2 * a,
    )


result = 1
for time, distance in races:
    a, b = roots(-1, time, -(distance + 0.00001))
    a = ceil(a)
    b = floor(b)
    result *= b - a + 1
print(result)

time_digits, distance_digits = zip(*races)
time, distance = (int("".join(map(str, digits))) for digits in (time_digits, distance_digits))

a, b = roots(-1, time, -(distance + 0.00001))
a = ceil(a)
b = floor(b)
print(b - a + 1)
