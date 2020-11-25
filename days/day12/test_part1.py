import pytest
from .day12lib import Moon, parse_input, simulate, moon_pairs


def test_apply_gravity():
    ganymede = Moon(3, 0, 0)
    callisto = Moon(5, 0, 0)
    Moon.apply_gravity(ganymede, callisto)
    assert ganymede.vx == 1
    assert callisto.vx == -1


def test_apply_velocity():
    europa = Moon(1, 2, 3, -2, 0, 3)
    europa.apply_velocity()
    assert europa.position == (-1, 2, 6)


def test_moon_pairs():
    moons = [
        Moon(-1, 0, 2),
        Moon(2, -10, -7),
        Moon(4, -8, 8),
        Moon(3, 5, -1),
    ]
    pairs = list(moon_pairs(moons))
    assert len(pairs) == 6
    assert pairs == [
        (moons[0], moons[1]),
        (moons[0], moons[2]),
        (moons[0], moons[3]),
        (moons[1], moons[2]),
        (moons[1], moons[3]),
        (moons[2], moons[3]),
    ]


@pytest.mark.parametrize(
    "data,steps,final_energy",
    [
        (
            """
            <x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>
            """,
            [
                [
                    Moon(2, -1, 1, 3, -1, -1),
                    Moon(3, -7, -4, 1, 3, 3),
                    Moon(1, -7, 5, -3, 1, -3),
                    Moon(2, 2, 0, -1, -3, 1),
                ],
                [
                    Moon(5, -3, -1, 3, -2, -2),
                    Moon(1, -2, 2, -2, 5, 6),
                    Moon(1, -4, -1, 0, 3, -6),
                    Moon(1, -4, 2, -1, -6, 2),
                ],
                [
                    Moon(5, -6, -1, 0, -3, 0),
                    Moon(0, 0, 6, -1, 2, 4),
                    Moon(2, 1, -5, 1, 5, -4),
                    Moon(1, -8, 2, 0, -4, 0),
                ],
                [
                    Moon(2, -8, 0, -3, -2, 1),
                    Moon(2, 1, 7, 2, 1, 1),
                    Moon(2, 3, -6, 0, 2, -1),
                    Moon(2, -9, 1, 1, -1, -1),
                ],
                [
                    Moon(-1, -9, 2, -3, -1, 2),
                    Moon(4, 1, 5, 2, 0, -2),
                    Moon(2, 2, -4, 0, -1, 2),
                    Moon(3, -7, -1, 1, 2, -2),
                ],
                [
                    Moon(-1, -7, 3, 0, 2, 1),
                    Moon(3, 0, 0, -1, -1, -5),
                    Moon(3, -2, 1, 1, -4, 5),
                    Moon(3, -4, -2, 0, 3, -1),
                ],
                [
                    Moon(2, -2, 1, 3, 5, -2),
                    Moon(1, -4, -4, -2, -4, -4),
                    Moon(3, -7, 5, 0, -5, 4),
                    Moon(2, 0, 0, -1, 4, 2),
                ],
                [
                    Moon(5, 2, -2, 3, 4, -3),
                    Moon(2, -7, -5, 1, -3, -1),
                    Moon(0, -9, 6, -3, -2, 1),
                    Moon(1, 1, 3, -1, 1, 3),
                ],
                [
                    Moon(5, 3, -4, 0, 1, -2),
                    Moon(2, -9, -3, 0, -2, 2),
                    Moon(0, -8, 4, 0, 1, -2),
                    Moon(1, 1, 5, 0, 0, 2),
                ],
                [
                    Moon(2, 1, -3, -3, -2, 1),
                    Moon(1, -8, 0, -1, 1, 3),
                    Moon(3, -6, 1, 3, 2, -3),
                    Moon(2, 0, 4, 1, -1, -1),
                ],
            ],
            179,
        ),
    ],
)
def test_step(data, steps, final_energy):
    moons = parse_input(data)
    for i, s in enumerate(steps):
        energy = simulate(moons, 1)
        assert moons == s, i + 1
    assert energy == final_energy
