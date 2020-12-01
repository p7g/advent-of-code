from .part2 import part2


def test_part2():
    assert 241861950 == part2(
        """
        1721
        979
        366
        299
        675
        1456
        """.strip().splitlines()
    )
