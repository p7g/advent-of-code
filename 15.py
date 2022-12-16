from aoc import *

sensors = set()
closest_beacon = {}
beacons = set()

for line in data.splitlines():
    coords = line[len("Sensor at "):].split(": closest beacon is at ", 1)

    sensor, beacon = (tuple(map(int, map(itemgetter(slice(2, None)), coord.split(", ")))) for coord in coords)
    sensors.add(sensor)
    beacons.add(beacon)
    closest_beacon[sensor] = beacon

minx, maxx = minmax(x for x, y in chain(sensors, beacons))
miny, maxy = minmax(y for x, y in chain(sensors, beacons))

y = 2_000_000
covers_y = set()
covered = set()
for sensor in sensors:
    beacon = closest_beacon[sensor]
    dist = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
    remaining_range = dist - abs(sensor[1] - y)
    if remaining_range < 0:
        continue
    for x in range(sensor[0] - remaining_range, sensor[0] + remaining_range + 1):
        if (x, y) not in sensors and (x, y) not in beacons:
            covered.add(x)

print(len(covered))

bound = 4_000_000
soln = None
for y in range(0, bound + 1):
    covered_ranges = []
    for sensor in sensors:
        beacon = closest_beacon[sensor]
        dist = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
        remaining_range = dist - abs(sensor[1] - y)
        if remaining_range < 0:
            continue
        covered_ranges.append((max(0, sensor[0] - remaining_range), min(bound, sensor[0] + remaining_range)))

    sorted_ranges = sorted(covered_ranges)
    non_overlapping_ranges = [sorted_ranges.pop(0)]
    for start, end in sorted_ranges:
        current = non_overlapping_ranges[-1]
        assert start >= current[0]
        if start >= current[0] and end <= current[1]:
            continue
        elif start <= current[1] and end > current[1]:
            non_overlapping_ranges[-1] = (current[0], end)
        else:
            non_overlapping_ranges.append((start, end))

    for a, b in pairwise(non_overlapping_ranges):
        if a[1] < b[0] - 1:
            soln = (a[1] + 1, y)
            break

    if soln is not None:
        break

if soln is None:
    raise Exception("no solution")
x, y = soln
print(x * 4_000_000 + y)
