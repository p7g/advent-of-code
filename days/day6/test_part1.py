import pytest
from .day6lib import parse_orbit, graph_from_input
from .part1 import number_of_orbits


@pytest.mark.parametrize(
    "raw,a,b",
    [
        ("COM)B", "COM", "B"),
        ("B)C", "B", "C"),
        ("C)D", "C", "D"),
        ("D)E", "D", "E"),
        ("E)F", "E", "F"),
    ],
)
def test_parse_orbit(raw, a, b):
    assert parse_orbit(raw) == (a, b)


def test_number_of_orbits():
    input = """
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
    """

    g = graph_from_input(input)
    assert number_of_orbits(g) == 42
