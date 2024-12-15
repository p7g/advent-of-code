from aoc import *

raw_map, raw_moves = data.split("\n\n")
moves = "".join(raw_moves.splitlines())
initial_grid = raw_map.splitlines()
dims = wh(initial_grid)

D = {
	"^": Pt(0, -1),
	">": Pt(1, 0),
	"v": Pt(0, 1),
	"<": Pt(-1, 0),
}
S = {
	"^": lambda pt: pt.y,
	">": lambda pt: -pt.x,
	"v": lambda pt: -pt.y,
	"<": lambda pt: pt.x,
}

map_ = [[t.cast(str | None, None)] * dims.x for _ in range(dims.y)]
for pt, c in pts(initial_grid):
	if c in "#O":
		pt.set(map_, c)
	elif c == "@":
		start_pos = pt

map2 = [[t.cast(str | None, None)] * 2 * dims.x for _ in range(dims.y)]
for pt, obj in pts(initial_grid):
	pt = Pt(pt.x * 2, pt.y)

	if obj == "#":
		pt.set(map2, "#")
		(pt + Pt(1, 0)).set(map2, "#")
	elif obj == "O":
		pt.set(map2, "[")
		(pt + Pt(1, 0)).set(map2, "]")
	elif obj == "@":
		start_pos = pt


def collect(map_, pos, direction):
	pos2 = pos + D[direction]
	obj = map_ @ pos2
	if obj is None:
		return {pos}, False
	elif obj == "#":
		return set(), True

	if obj == "O":
		pts, blocked = collect(map_, pos2, direction)
		return {pos} | pts, blocked
	elif obj == "[":
		left = pos2
		right = pos2 + Pt(1, 0)
	else:
		left = pos2 - Pt(1, 0)
		right = pos2

	move = {pos, left, right}
	if direction == ">":
		pts, blocked = collect(map_, right, direction)
		return move | pts, blocked
	elif direction == "<":
		pts, blocked = collect(map_, left, direction)
		return move | pts, blocked
	else:
		pts1, blocked1 = collect(map_, left, direction)
		pts2, blocked2 = collect(map_, right, direction)
		return move | pts1 | pts2, blocked1 or blocked2


def run(map_):
	robot = start_pos
	for direction in moves:
		to_move, blocked = collect(map_, robot, direction)
		if blocked:
			continue
		for pt in sorted(to_move, key=S[direction]):
			c = map_ @ pt
			pt.set(map_, None)
			pt += D[direction]
			pt.set(map_, c)
		robot += D[direction]

	print(sum(100 * pt.y + pt.x for pt, obj in pts(map_) if obj in ("[", "O")))


run(map_)
run(map2)
