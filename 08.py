from aoc import *

steps, node_defs = data.split("\n\n")

nodes = {}
for node in node_defs.splitlines():
    name, nbrs = node.split(" = ", 1)
    nodes[name] = tuple(nbrs.strip("()").split(", "))

pos = "AAA"

dirs = cycle(steps)
nsteps = 0
while pos != "ZZZ":
    dir = next(dirs)
    pos = nodes[pos][dir == "R"]
    nsteps += 1

print(nsteps)

start_positions = [node for node in nodes if node.endswith("A")]
end_nsteps = set()

for start_position in start_positions:
    pos = start_position

    dirs = cycle(steps)
    nsteps = 0
    while not pos.endswith("Z"):
        dir = next(dirs)
        pos = nodes[pos][dir == "R"]
        nsteps += 1

    end_nsteps.add(nsteps)

print(lcm(*end_nsteps))
