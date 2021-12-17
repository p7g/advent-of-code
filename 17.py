from aoc import *

xspec, yspec = data.split(": ")[1].split(", ")
xmin, xmax = tuple(map(int, xspec.removeprefix("x=").split("..")))
ymin, ymax = tuple(map(int, yspec.removeprefix("y=").split("..")))


def height(yv):
    h = pos = 0
    while pos >= ymin:
        pos += yv
        yv -= 1
        if pos > h:
            h = pos
        if ymin <= pos <= ymax:
            return h
    return None


yvel = -ymin - 1
print(height(yvel))


def reaches_target(xvel, yvel):
    xpos, ypos = 0, 0

    while xpos <= xmax and ypos >= ymin:
        if xmin <= xpos <= xmax and ymin <= ypos <= ymax:
            return True
        xpos += xvel
        xvel -= 1 * sign(xvel)
        ypos += yvel
        yvel -= 1

    return False


nvalid = 0
for y in range(-yvel - 1, yvel + 1):
    for x in range(1, xmax + 1):
        nvalid += reaches_target(x, y)

print(nvalid)
