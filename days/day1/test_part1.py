from .part1 import part1


def test_part1():
    assert 514579 == part1(
        """
        1721
        979
        366
        299
        675
        1456
        """.strip().splitlines()
    )
