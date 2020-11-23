from .day6lib import graph_from_input
from .part2 import number_of_transfers


def test_number_of_transfers():
    input_ = """
    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN
    """

    g = graph_from_input(input_)
    assert number_of_transfers(g) == 4
