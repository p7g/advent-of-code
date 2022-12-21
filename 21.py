from aoc import *
import networkx as nx

G = nx.DiGraph()

for line in data.splitlines():
    name, rhs = line.split(": ")

    G.add_node(name)
    if rhs.isnumeric():
        G.nodes[name]["value"] = int(rhs)
    else:
        lhs, op_str, rhs = rhs.split(" ", 2)
        G.nodes[name]["op"] = {"*": op.mul, "/": op.floordiv, "+": op.add, "-": op.sub}[op_str]
        G.add_edge(name, lhs)
        G.nodes[lhs]["side"] = "left"
        G.add_edge(name, rhs)
        G.nodes[rhs]["side"] = "right"

assert nx.is_tree(G)


def value(node):
    if "value" in G.nodes[node]:
        return G.nodes[node]["value"]
    return reduce(G.nodes[node]["op"], map(value, G.succ[node]))


print(value("root"))

G.nodes["humn"]["value"] = None
target_value = subtree = None

for node in G.succ["root"]:
    if "humn" in nx.descendants(G, node):
        subtree = node
    else:
        target_value = value(node)
assert target_value is not None and subtree is not None


def yell_what(node, expected_value):
    if "value" in G.nodes[node]:
        val = G.nodes[node]["value"]
        assert node == "humn" and val is None
        return expected_value

    op_ = G.nodes[node]["op"]
    other = incomplete = None
    for succ in G.succ[node]:
        if succ == "humn" or "humn" in nx.descendants(G, succ):
            incomplete = succ
        else:
            other = value(succ)
    assert other is not None and incomplete is not None

    if op_ == op.add:
        next_target = expected_value - other
    elif op_ == op.sub:
        if G.nodes[incomplete]["side"] == "left":
            next_target = expected_value + other
        else:
            next_target = other - expected_value
    elif op_ == op.mul:
        next_target = expected_value // other
    elif op_ == op.floordiv:
        if G.nodes[incomplete]["side"] == "left":
            next_target = expected_value * other
        else:
            next_target = other // expected_value
    else:
        raise NotImplementedError(op)

    return yell_what(incomplete, next_target)


print(yell_what(subtree, target_value))
