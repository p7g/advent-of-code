from aoc import *

grid = data.splitlines()
dims = wh(grid)


def perimeter(plot, region=None):
    region = region or set()
    ty = plot.get(grid)
    p = 0
    region.add(plot)

    for pt in plot.nbrs4():
        if not pt.inbound(dims) or pt.get(grid) != ty:
            p += 1
        elif pt in region:
            continue
        else:
            p2, r2 = perimeter(pt, region)
            p += p2
            region.update(r2)

    return p, region


all_seen = set()
regions = []
cost = 0
for pt, type_ in pts(grid):
    if pt in all_seen:
        continue
    p, region = perimeter(pt)
    all_seen.update(region)
    cost += p * len(region)
    regions.append((type_, region))

print(cost)


def isother(pt, ty):
    return not pt.inbound(dims) or pt.get(grid) != ty


cost = 0
for ty, region in regions:
    corners = 0
    for pt in region:
        UL, L, DL, U, D, UR, R, DR = map(partial(isother, ty=ty), pt.nbrs8())
        corners += D == R if DR else D and R
        corners += D == L if DL else D and L
        corners += U == L if UL else U and L
        corners += U == R if UR else U and R
    cost += len(region) * corners

print(cost)
