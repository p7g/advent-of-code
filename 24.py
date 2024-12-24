import networkx as nx

from aoc import *


class Gate:
    def __init__(self, operator, operands, output, dependencies):
        self.operator = operator
        self.operands = operands
        self.output = output
        self.dependencies = dependencies


initial_values_str, gates_str = data.split("\n\n", 1)
ops = {"AND": op.and_, "OR": op.or_, "XOR": op.xor}
all_wires = set()
gates = []
dependents = defaultdict(list)
provides = {}

initial_values = {}
for line in initial_values_str.splitlines():
    wire, value_str = line.split(": ", 1)
    initial_values[wire] = int(value_str)
    all_wires.add(wire)

for line in gates_str.splitlines():
    a, op_, b, _, dest = line.split(" ")
    gate = Gate(ops[op_], [], dest, (a, b))
    dependents[a].append(gate)
    dependents[b].append(gate)
    provides[dest] = gate
    gates.append(gate)
    all_wires.update((a, b, dest))


def eval_gates(initial_values):
    for gate in gates:
        gate.operands.clear()

    wire_values = {}
    ready_gates = deque()
    for wire, value in initial_values.items():
        wire_values[wire] = value
        for gate in dependents[wire]:
            gate.operands.append(value)
            if len(gate.operands) == 2:
                ready_gates.append(gate)

    while ready_gates:
        gate = ready_gates.popleft()
        a, b = gate.operands
        value = gate.operator(a, b)
        wire_values[gate.output] = value
        for gate in dependents[gate.output]:
            gate.operands.append(value)
            if len(gate.operands) == 2:
                ready_gates.append(gate)

    return wire_values


nbits = max(int(w[1:]) for w in all_wires if w[0] == "x") + 1


def parse_result(wire_values):
    s = 0
    for i in range(nbits, -1, -1):
        s <<= 1
        s |= wire_values[f"z{i:02}"]
    return s


print(parse_result(eval_gates(initial_values)))


def make_input(a, b):
    input_ = {}
    for i in range(nbits):
        n = a & 1
        input_[f"x{i:02}"] = n
        a >>= 1
    for i in range(nbits):
        n = b & 1
        input_[f"y{i:02}"] = n
        b >>= 1
    return input_


def swap_outputs(a, b):
    a.output, b.output = b.output, a.output
    provides[a.output] = a
    provides[b.output] = b


swap_outputs(provides["fph"], provides["z15"])
swap_outputs(provides["gds"], provides["z21"])
swap_outputs(provides["wrk"], provides["jrs"])
swap_outputs(provides["cqk"], provides["z34"])

G = nx.DiGraph()
for gate in gates:
    G.add_node(gate.output, label=f"{gate.operator.__name__} -> {gate.output}")
    G.add_edges_from((dep, gate.output) for dep in gate.dependencies)

nx.nx_pydot.write_dot(G, "24.dot")

prev = None
for i in range(nbits):
    test_cases = [
        (0 << i, 0 << i, 0 << i),
        (0 << i, 1 << i, 1 << i),
        (1 << i, 0 << i, 1 << i),
        (1 << i, 1 << i, 2 << i),
    ]
    for a, b, expected in test_cases:
        result = parse_result(eval_gates(make_input(a, b)))
        if result != expected:
            print()
            print(i)
            print(f"{a=} {b=} {expected=} {result=}")
            input()

print(",".join(sorted(("fph", "z15", "gds", "z21", "wrk", "jrs", "cqk", "z34"))))
