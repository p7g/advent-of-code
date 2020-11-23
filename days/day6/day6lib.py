import networkx as nx


def parse_orbit(s):
    left, right = [], []
    parsing_left = True
    for c in s.strip():
        if c == ")":
            parsing_left = False
            continue
        (left if parsing_left else right).append(c)
    return "".join(left), "".join(right)


def graph_from_input(raw_input):
    return nx.Graph(
        map(
            lambda s: tuple(reversed(s)),
            map(parse_orbit, raw_input.strip().splitlines()),
        )
    )
