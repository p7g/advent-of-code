from aoc import *
import networkx as nx

TIME_LIMIT = 30
G = nx.Graph()
worth_opening = set()

for line in data.splitlines():
    a, b = line.split("; ", 1)
    valve, _ = a[len("Valve ") :].split(" ", 1)
    flow_rate = int(a.rsplit("=", 1)[-1])
    dests = re.sub(r"^tunnels? leads? to valves? ", "", b).split(", ")
    G.add_node(valve)
    G.nodes[valve]["flow_rate"] = flow_rate
    G.add_edges_from((valve, dest) for dest in dests)
    if flow_rate:
        worth_opening.add(valve)


@cache
def shortest_path(src, dest):
    return nx.shortest_path(G, src, dest)[1:]


@dataclass(frozen=True)
class State:
    location: str
    elapsed_time: int
    opened_valves: "frozenset[str]"
    pressure_released: int

    @property
    def pressure_released_per_minute(self) -> int:
        return sum(G.nodes[v]["flow_rate"] for v in self.opened_valves)

    def estimate_total_released_pressure(self) -> int:
        return self.pressure_released + self.pressure_released_per_minute * (
            TIME_LIMIT - self.elapsed_time
        )

    def next_states(self) -> t.Iterable["State"]:
        if self.elapsed_time == TIME_LIMIT:
            return
        assert self.elapsed_time < TIME_LIMIT

        had_any = False
        for closed_valve in worth_opening - self.opened_valves:
            distance = len(shortest_path(self.location, closed_valve))
            time_needed = distance + 1  # open the valve
            if self.elapsed_time + time_needed > TIME_LIMIT:
                continue
            had_any = True
            pressure_released = (
                self.pressure_released + time_needed * self.pressure_released_per_minute
            )
            yield State(
                closed_valve,
                self.elapsed_time + time_needed,
                self.opened_valves | {closed_valve},
                pressure_released,
            )

        if not had_any:
            yield State(
                self.location,
                TIME_LIMIT,
                self.opened_valves,
                self.estimate_total_released_pressure(),
            )

    def next_states2(self) -> t.Iterable["State"]:
        if self.elapsed_time == TIME_LIMIT:
            return
        assert self.elapsed_time < TIME_LIMIT

        moves = list(G.adj[self.location])
        if self.location in worth_opening and self.location not in self.opened_valves:
            moves.append("open")

        for move in moves:
            elapsed_time = self.elapsed_time + 1
            opened_valves = self.opened_valves
            if move == "open":
                opened_valves |= {self.location}
            location = self.location if move == "open" else move
            released_pressure = (
                self.pressure_released + self.pressure_released_per_minute
            )
            yield State(
                location,
                elapsed_time,
                opened_valves,
                released_pressure,
            )


states = [State("AA", 0, frozenset(), 0)]
seen_states = set(states)
final_states = set()

while states:
    state = states.pop()
    seen_states.add(state)
    next_states = list(state.next_states())
    if not next_states:
        final_states.add(state)
    else:
        states.extend(st for st in next_states if st not in seen_states)

print(max(final_states, key=attrgetter("pressure_released")).pressure_released)

del seen_states, final_states
TIME_LIMIT = 26

states = [State("AA", 0, frozenset(), 0)]
seen_states = set(states)
final_states = set()

while states:
    state = states.pop()
    seen_states.add(state)
    next_states = list(state.next_states2())
    if not next_states:
        final_states.add(state)
    else:
        states.extend(st for st in next_states if st not in seen_states)

best_by_opened_valves = {}
for state in seen_states:
    if (
        state.opened_valves not in best_by_opened_valves
        or state.pressure_released > best_by_opened_valves[state.opened_valves]
    ):
        best_by_opened_valves[state.opened_valves] = state.pressure_released

print(
    max(
        best_by_opened_valves[a] + best_by_opened_valves[b]
        for a, b in combinations(best_by_opened_valves.keys(), 2)
        if a.isdisjoint(b)
    )
)
