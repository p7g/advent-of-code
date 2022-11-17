from aoc import *

part2 = True
if part2:
    extra = """\
  #D#C#B#A#
  #D#B#A#C#\
"""
    data_lines = data.splitlines()
    data = "\n".join(data_lines[:3] + extra.splitlines() + data_lines[-2:])


COST = dict(zip("ABCD", [1, 10, 100, 1000]))
DEST_ROOM = dict((c, i) for i, c in enumerate("ABCD"))
ROOM_POS = dict((i, i * 2 + 2) for i in range(4))
ROOM_SIZE = len(data.splitlines()) - 3

num = [count() for _ in range(4)]
ROOM_LINES = [
    tuple(
        (variant, ("room", (i, next(num[i]))))
        for i, variant in enumerate(l[3:10].split("#"))
    )
    for l in data.splitlines()[2:-1]
]


def guess_solution_cost(state):
    amphipods = state[-1]

    cost = 0

    next_room_pos = dict(zip("ABCD", [3, 3, 3, 3]))
    for variant, pos in amphipods:
        if pos[0] == "room":
            room_idx, pos_in_room = pos[1]
            if room_idx == DEST_ROOM[variant]:
                cost += (next_room_pos[variant] - pos_in_room) * COST[variant]
                next_room_pos[variant] -= 1
                continue
            cost += (pos_in_room + 1 + abs(ROOM_POS[room_idx] - ROOM_POS[DEST_ROOM[variant]]) + next_room_pos[variant] + 1) * COST[variant]
            next_room_pos[variant] -= 1
        else:
            pos_in_hall = pos[1]
            cost += (abs(pos_in_hall - ROOM_POS[DEST_ROOM[variant]]) + next_room_pos[variant] + 1) * COST[variant]
            next_room_pos[variant] -= 1

    return cost


def print_state(state):
    hallway, rooms, _ = state
    print("#" * len(data.splitlines()[0]))
    print("#" + "".join(("." if x is None else x[0]) for x in hallway) + "#")
    first = True
    for i in range(ROOM_SIZE):
        s = "###" if first else "  #"
        for room in rooms:
            occupant = room[i]
            s += occupant[0] if occupant else "."
            s += "#"
        s += "##" if first else "  "
        print(s)
        first = False
    print("  " + "#" * (len(data.splitlines()[0]) - 4) + "  ")


def main():
    @dataclass
    @total_ordering
    class Node:
        state: tuple

        @property
        def guessed_total_energy(self) -> int:
            return guessed_total_energy[self.state]

        def __lt__(self, other):
            return self.guessed_total_energy < other.guessed_total_energy

    initial_state = (
        tuple([None] * (len(data.splitlines()[1]) - 2)),
        tuple(zip(*ROOM_LINES)),
        tuple(it.flatten(ROOM_LINES)),
    )

    energy_so_far = defaultdict(lambda: float("inf"), {initial_state: 0})
    guessed_total_energy = defaultdict(lambda: float("inf"), {initial_state: guess_solution_cost(initial_state)})
    # yes i referred to wikipedia
    open_set = [Node(initial_state)]
    open_set_set = {initial_state}
    pred = {}

    while open_set:
        node = heappop(open_set)
        hallway, rooms, amphipods = node.state
        open_set_set.remove(node.state)

        if all(
            all(room)
            and all(a[0] == b[0] == "ABCD"[i] for a, b in it.pairwise(room))
            for i, room in enumerate(rooms)
        ):
            end_state = node.state
            break

        possible_next_states = []

        for a_idx, a in enumerate(amphipods):
            location, idx = a[1]
            if location == "room":
                room_idx, idx_in_room = idx
                if idx_in_room != 0 and any(rooms[room_idx][:idx_in_room]):
                    possible_dests = []  # Blocked
                elif room_idx == DEST_ROOM[a[0]] and all(
                    b[0] == a[0] for b in rooms[room_idx] if b
                ):
                    possible_dests = []  # Already done
                else:
                    possible_dests = []
                    reached_room = False
                    for i, occupant in enumerate(hallway):
                        if not occupant:
                            if i not in ROOM_POS.values():
                                possible_dests.append((("hall", i), idx_in_room + 1 + abs(ROOM_POS[room_idx] - i)))
                            elif i == ROOM_POS[room_idx]:
                                reached_room = True
                        elif not reached_room:
                            possible_dests.clear()
                        else:
                            break
                    # Can also move directly into room, this probably never
                    # happens because moving into the hallway costs less
                    if all(occupant[0] == a[0] for occupant in rooms[DEST_ROOM[a[0]]] if occupant):
                        start, end = sorted([ROOM_POS[room_idx], ROOM_POS[DEST_ROOM[a[0]]]])
                        if all(hallway[pos] is None for pos in range(start, end)):
                            pos_in_room = next(i for i, occupant in reversed(list(enumerate(rooms[DEST_ROOM[a[0]]]))) if occupant is None)
                            move_cost = (idx_in_room + 1 + (end - start) + pos_in_room + 1) * COST[a[0]]
                            possible_dests.append(
                                (("room", (DEST_ROOM[a[0]], pos_in_room)), move_cost)
                            )
            elif location == "hall":
                dest_room_pos = ROOM_POS[DEST_ROOM[a[0]]]
                if any(
                    occupant is not None and occupant[0] != a[0]
                    for occupant in rooms[DEST_ROOM[a[0]]]
                ):
                    possible_dests = []  # Can't go into room yet
                elif any(
                    hallway[idx + 1 : dest_room_pos]
                    if idx < dest_room_pos
                    else hallway[dest_room_pos:idx]
                ):
                    possible_dests = []  # Hallway blocked
                else:
                    first_open_spot = (
                        next(
                            (
                                i
                                for i, o in enumerate(rooms[DEST_ROOM[a[0]]])
                                if o is not None
                            ),
                            len(rooms[0]),
                        )
                        - 1
                    )
                    possible_dests = [
                        (
                            (
                                "room",
                                (
                                    DEST_ROOM[a[0]],
                                    first_open_spot,
                                ),
                            ),
                            abs(dest_room_pos - idx) + 1 + first_open_spot,
                        ),
                    ]

            for newpos, moved_places in possible_dests:
                newa = (a[0], newpos)
                new_hallway = list(hallway)
                new_rooms = list(rooms)
                new_amphipods = list(amphipods)
                move_cost = COST[a[0]] * moved_places

                # replace a in amphipods list

                if a[1][0] == "room":
                    r_id, id_in_r = a[1][1]
                    r = list(new_rooms[r_id])
                    r[id_in_r] = None
                    new_rooms[r_id] = tuple(r)
                else:
                    new_hallway[a[1][1]] = None
                if newpos[0] == "room":
                    r_id, id_in_r = newpos[1]
                    r = list(new_rooms[r_id])
                    r[id_in_r] = newa
                    new_rooms[r_id] = tuple(r)
                else:
                    new_hallway[newpos[1]] = newa

                new_amphipods[a_idx] = newa

                new_state = (
                    tuple(new_hallway),
                    tuple(new_rooms),
                    tuple(new_amphipods),
                )
                possible_next_states.append((new_state, move_cost))

        for next_state, move_cost in possible_next_states:
            total_cost = energy_so_far[node.state] + move_cost
            if total_cost < energy_so_far[next_state]:
                energy_so_far[next_state] = total_cost
                guessed_total_energy[next_state] = total_cost + guess_solution_cost(next_state)
                pred[next_state] = node.state
                if next_state not in open_set_set:
                    heappush(open_set, Node(next_state))
                    open_set_set.add(next_state)
    else:
        raise Exception("No solution")


    print(energy_so_far[end_state])
    path = [end_state]
    while path[-1] != initial_state:
        path.append(pred[path[-1]])
    path.reverse()

    for node in path:
        print_state(node)
        print()


main()
