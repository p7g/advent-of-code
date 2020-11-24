from .day10lib import parse_points
from .part2 import destruction_order


def test_part2():
    data = """
    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##
    """

    ps = parse_points(data)
    order = list(destruction_order((11, 13), ps))

    assert len(order) == 299
    assert order[0] == (11, 12)
    assert order[1] == (12, 1)
    assert order[2] == (12, 2)
    assert order[9] == (12, 8)
    assert order[19] == (16, 0)
    assert order[49] == (16, 9)
    assert order[99] == (10, 16)
    assert order[198] == (9, 6)
    assert order[199] == (8, 2)
    assert order[200] == (10, 9)
    assert order[298] == (11, 1)
