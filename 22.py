from aoc import *

steps = [
    (st == "on", tuple(tuple(map(int, r[2:].split(".."))) for r in ranges.split(",")))
    for st, ranges in map(methodcaller("split", " "), data.splitlines())
]

cubes = {}

for new_state, ranges in steps:
    if any(abs(bound) > 50 for bound in it.flatten(ranges)):
        continue

    (xmin, xmax), (ymin, ymax), (zmin, zmax) = ranges

    for pt in product(
        range(xmin, xmax + 1), range(ymin, ymax + 1), range(zmin, zmax + 1)
    ):
        cubes[pt] = new_state

print(sum(cubes.values()))


def region_volume(region):
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = region
    return (xmax - xmin + 1) * (ymax - ymin + 1) * (zmax - zmin + 1)


on_regions = []

for stepno, (new_state, ranges) in enumerate(steps):
    if new_state and not on_regions:
        on_regions.append(ranges)
        continue

    work_queue = [ranges]

    while work_queue:
        new_on_regions = []
        ranges = work_queue.pop()
        (xmin, xmax), (ymin, ymax), (zmin, zmax) = ranges

        for i, region in enumerate(on_regions):
            if (
                xmin <= region[0][0]
                and xmax >= region[0][1]
                and ymin <= region[1][0]
                and ymax >= region[1][1]
                and zmin <= region[2][0]
                and zmax >= region[2][1]
            ):
                # fully covers
                work_queue.append(ranges)  # remove region from on_regions
                new_on_regions.extend(on_regions[i + 1 :])
                break
            elif (
                xmin >= region[0][0]
                and xmax <= region[0][1]
                and ymin >= region[1][0]
                and ymax <= region[1][1]
                and zmin >= region[2][0]
                and zmax <= region[2][1]
            ):
                # fully covered
                if new_state:
                    new_on_regions.extend(on_regions[i:])
                    break

            if not (
                xmin <= region[0][1]
                and xmax >= region[0][0]
                and ymin <= region[1][1]
                and ymax >= region[1][0]
                and zmin <= region[2][1]
                and zmax >= region[2][0]
            ):
                # no overlap
                new_on_regions.append(region)
                continue

            if new_state:
                if xmin < region[0][0]:
                    ltx_region = (
                        (xmin, region[0][0] - 1),
                        (ymin, ymax),
                        (zmin, zmax),
                    )
                    work_queue.append(ltx_region)

                if xmax > region[0][1]:
                    gtx_region = (
                        (region[0][1] + 1, xmax),
                        (ymin, ymax),
                        (zmin, zmax),
                    )
                    work_queue.append(gtx_region)

                if ymin < region[1][0]:
                    lty_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (ymin, region[1][0] - 1),
                        (zmin, zmax),
                    )
                    work_queue.append(lty_region)

                if ymax > region[1][1]:
                    gty_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (region[1][1] + 1, ymax),
                        (zmin, zmax),
                    )
                    work_queue.append(gty_region)

                if zmin < region[2][0]:
                    ltz_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (max(ymin, region[1][0]), min(ymax, region[1][1])),
                        (zmin, region[2][0] - 1),
                    )
                    work_queue.append(ltz_region)

                if zmax > region[2][1]:
                    gtz_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (max(ymin, region[1][0]), min(ymax, region[1][1])),
                        (region[2][1] + 1, zmax),
                    )
                    work_queue.append(gtz_region)

                new_on_regions.extend(on_regions[i:])
                break
            else:
                if region[0][0] < xmin:
                    ltx_region = (
                        (region[0][0], xmin - 1),
                        region[1],
                        region[2],
                    )
                    new_on_regions.append(ltx_region)

                if region[0][1] > xmax:
                    gtx_region = (
                        (xmax + 1, region[0][1]),
                        region[1],
                        region[2],
                    )
                    new_on_regions.append(gtx_region)

                if region[1][0] < ymin:
                    lty_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (region[1][0], ymin - 1),
                        region[2],
                    )
                    new_on_regions.append(lty_region)

                if region[1][1] > ymax:
                    gty_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (ymax + 1, region[1][1]),
                        region[2],
                    )
                    new_on_regions.append(gty_region)

                if region[2][0] < zmin:
                    ltz_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (max(ymin, region[1][0]), min(ymax, region[1][1])),
                        (region[2][0], zmin - 1),
                    )
                    new_on_regions.append(ltz_region)

                if region[2][1] > zmax:
                    gtz_region = (
                        (max(xmin, region[0][0]), min(xmax, region[0][1])),
                        (max(ymin, region[1][0]), min(ymax, region[1][1])),
                        (zmax + 1, region[2][1]),
                    )
                    new_on_regions.append(gtz_region)
        else:
            if new_state:
                new_on_regions.append(ranges)

        on_regions = list(new_on_regions)


print(sum(map(region_volume, on_regions)))
