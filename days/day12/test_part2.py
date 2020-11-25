from .part2 import find_repeated_universe, parse_input


def test_find_repeated_universe():
    moons = parse_input(
        """
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
        """
    )

    assert find_repeated_universe(moons) == 4686774924
