from aoc import *

row_obstacles = defaultdict(list)
col_obstacles = defaultdict(list)
grid = data.splitlines()
W, H = wh(grid)

for y, row in enumerate(grid):
    for x, tile in enumerate(row):
        if tile == "#":
            row_obstacles[y].append(x)
            col_obstacles[x].append(y)
        elif tile == "^":
            guard_start = Pt(x, y)

guard_pos = guard_start
direction = "up"
lines = []

for i in count():
    x, y = guard_pos
    done = False
    if direction == "up":
        obstacles = col_obstacles[x]
        idx = bisect_right(obstacles, y)
        if idx == 0:
            done = True
            guard_pos = Pt(x, -1)
        else:
            guard_pos = Pt(x, obstacles[idx - 1] + 1)
        direction = "right"
    elif direction == "right":
        obstacles = row_obstacles[y]
        idx = bisect_left(obstacles, x)
        if idx == len(obstacles):
            done = True
            guard_pos = Pt(W, y)
        else:
            guard_pos = Pt(obstacles[idx] - 1, y)
        direction = "down"
    elif direction == "down":
        obstacles = col_obstacles[x]
        idx = bisect_left(obstacles, y)
        if idx == len(obstacles):
            done = True
            guard_pos = Pt(x, H)
        else:
            guard_pos = Pt(x, obstacles[idx] - 1)
        direction = "left"
    elif direction == "left":
        obstacles = row_obstacles[y]
        idx = bisect_right(obstacles, x)
        if idx == 0:
            done = True
            guard_pos = Pt(-1, y)
        else:
            guard_pos = Pt(obstacles[idx - 1] + 1, y)
        direction = "up"

    lines.append((Pt(x, y), guard_pos))
    if done:
        break

seen = set()
for (x, y), guard_pos in lines:
    if x == guard_pos.x:
        for y in range(y, guard_pos.y, sign(guard_pos.y - y)):
            seen.add(Pt(x, y))
    elif y == guard_pos.y:
        for x in range(x, guard_pos.x, sign(guard_pos.x - x)):
            seen.add(Pt(x, y))

print(len(seen))


def simulate(obstacle_pos):
    guard_pos = tuple(globals()["guard_start"])
    row_obstacles = globals()["row_obstacles"].copy()
    col_obstacles = globals()["col_obstacles"].copy()
    x, y = obstacle_pos
    row_obstacles[y] = row_obstacles[y].copy()
    col_obstacles[x] = col_obstacles[x].copy()
    insort(row_obstacles[y], x)
    insort(col_obstacles[x], y)

    direction = "up"
    turns = set()

    while True:
        prev_direction = direction
        x, y = guard_pos
        if direction == "up":
            obstacles = col_obstacles[x]
            idx = bisect_right(obstacles, y)
            if idx == 0:
                return False
            else:
                guard_pos = (x, obstacles[idx - 1] + 1)
            direction = "right"
        elif direction == "right":
            obstacles = row_obstacles[y]
            idx = bisect_left(obstacles, x)
            if idx == len(obstacles):
                return False
            else:
                guard_pos = (obstacles[idx] - 1, y)
            direction = "down"
        elif direction == "down":
            obstacles = col_obstacles[x]
            idx = bisect_left(obstacles, y)
            if idx == len(obstacles):
                return False
            else:
                guard_pos = (x, obstacles[idx] - 1)
            direction = "left"
        elif direction == "left":
            obstacles = row_obstacles[y]
            idx = bisect_right(obstacles, x)
            if idx == 0:
                return False
            else:
                guard_pos = (obstacles[idx - 1] + 1, y)
            direction = "up"

        turn = (guard_pos, direction)
        if turn in turns:
            return True
        turns.add(turn)


n = 0
for p in seen:
    if p == guard_start:
        continue
    if simulate(p):
        n += 1
print(n)
