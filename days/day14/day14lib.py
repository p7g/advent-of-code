import re
import networkx as nx

unit_re = re.compile(r"(\d+) ([A-Z]+)")


def parse_input(data):
    rules = []

    for line in data.strip().splitlines():
        line = line.strip()
        inputs, output = map(str.strip, line.split("=>"))
        inputs = map(str.strip, inputs.split(","))

        m = unit_re.fullmatch(output)
        output = (int(m[1]), m[2])

        inputs2 = []
        for input_ in inputs:
            m = unit_re.fullmatch(input_)
            inputs2.append((int(m[1]), m[2]))

        rules.append((inputs2, output))

    return rules


def build_graph(rules):
    G = nx.DiGraph()

    for inputs, (nout, tout) in rules:
        G.add_node(tout, amount=nout)
        for nin, tin in inputs:
            G.add_edge(tin, tout, amount=nin)

    return G
