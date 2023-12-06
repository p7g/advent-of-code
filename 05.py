# from aoc import *

from more_itertools import chunked

with open(".aoc-cache/2023-5.txt") as f:
    data = f.read().strip()

seeds_raw, *maps_raw = data.split("\n\n")

seeds = [int(x) for x in seeds_raw.split(": ", 1)[1].split()]

maps = []
for map_raw in maps_raw:
    map_ = []
    header, *mappings = map_raw.splitlines()
    for line in mappings:
        map_.append(tuple(int(x) for x in line.split()))
    maps.append(map_)


lowest = float("inf")
for seed in seeds:
    value = seed
    for map_ in maps:
        for dst_start, src_start, length in map_:
            if src_start <= value < src_start + length:
                value = dst_start + (value - src_start)
                break
    lowest = min(lowest, value)

print(lowest)


class Range:
    __slots__ = ("start", "length")

    def __init__(self, start, length):
        self.start = start
        self.length = length

    @property
    def end(self):
        return self.start + self.length

    def overlaps(self, other):
        return (self.start < other.start < self.end) or (other.start < self.start < other.end)

    def __and__(self, other):
        assert self.overlaps(other)
        return Range(max(self.start, other.start), min(self.end, other.end) - max(self.start, other.start))

    def increment_start(self, delta):
        return Range(self.start + delta, self.length)

    def __iter__(self):
        yield from range(self.start, self.end)


for map_ in maps:
    map_.sort(key=lambda x: x[1])


def map_range(range, map_id=0):
    if map_id == len(maps):
        yield range
        return

    mappings = maps[map_id]
    dst_start, src_start, mapping_length = mappings[0]

    range_before = Range(0, src_start)
    if range.overlaps(range_before):
        yield from map_range(range & range_before, map_id + 1)

    for dst_start, src_start, mapping_length in mappings:
        src_range = Range(src_start, mapping_length)
        if not src_range.overlaps(range):
            continue

        yield from map_range((src_range & range).increment_start(dst_start - src_start), map_id + 1)

    dst_start, src_start, mapping_length = mappings[-1]
    range_after = Range(src_start + mapping_length, range.end)
    if range.overlaps(range_after):
        yield from map_range(range & range_after, map_id + 1)


print(min(i for start, length in chunked(seeds, 2) for r in map_range(Range(start, length)) for i in r))
