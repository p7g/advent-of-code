from aoc import *

rocks = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split("\n\n")

parsed_rocks = []
for rock in rocks:
	rows = rock.splitlines()
	height = len(rows)
	width = len(rows[0])

	rock = [[False] * width for _ in range(height)]
	for y, row in enumerate(rows):
		for x, c in enumerate(row):
			rock[y][x] = c == "#"

	parsed_rocks.append(rock)

rocks = parsed_rocks


def collision(rock, pos):
	x, y = pos
	for i in range(y, y + len(rock)):
		if i < 0:
			continue
		for j in range(x, x + len(rock[0])):
			if rock[i-y][j-x] and pile[i][j]:
				return True


for part in [1, 2]:
	falling_rocks = cycle(enumerate(rocks))
	jet_pattern = cycle(enumerate(-1 if c == "<" else 1 for c in data))
	pile = deque()
	seen_states = {}
	target = 1_000_000_000_000
	found_pattern = False

	jet_pattern_id = 0
	rockno = 0
	while True:
		rockno += 1
		if part == 1 and rockno == 2023:
			print(len(pile))
			break
		elif part == 2 and rockno == target + 1:
			print(len(pile) - 20 + extra_height)
			break

		x = 2
		rock_id, rock = next(falling_rocks)

		state = rock_id, jet_pattern_id, tuple(tuple(row) for row in take(20, pile))
		if not found_pattern and part == 2:
			if state in seen_states:
				offset, height_offset = seen_states[state]
				delta_height = len(pile) - height_offset
				length = rockno - offset
				nrepetitions = (target - offset) // length
				rockno = offset + nrepetitions * length
				extra_height = height_offset + nrepetitions * delta_height

				pile = deque(take(20, pile))
				found_pattern = True
			else:
				seen_states[state] = (rockno, len(pile))

		def next_x():
			global jet_pattern_id
			jet_pattern_id, movement = next(jet_pattern)
			new_x = x + movement
			minx, maxx = new_x, new_x + len(rock[0]) - 1
			between_walls = minx >= 0 and maxx < 7
			if not between_walls:
				return x
			return x if collision(rock, (new_x, y)) else new_x

		y = -len(rock) - 3

		while True:
			had_collision = False
			x = next_x()
			if y + len(rock) >= len(pile):
				break
			y += 1
			if collision(rock, (x, y)):
				y -= 1
				break

		while y < 0:
			pile.appendleft([False] * 7)
			y += 1

		for i in range(y, y + len(rock)):
			for j in range(x, x + len(rock[0])):
				if rock[i-y][j-x]:
					pile[i][j] = True

