from __future__ import annotations

from aoc import *


Sign = t.Literal[1, -1]
Point = t.Tuple[int, int, int]
PointIndex = t.Literal[0, 1, 2]
Rotation = t.Tuple[PointIndex, PointIndex, PointIndex]


class Orientation(t.NamedTuple):
    signs: t.Tuple[Sign, Sign, Sign]
    rotation: Rotation


all_orientations: t.Sequence[Orientation] = list(
    Orientation(*o)
    for o in product(product((1, -1), repeat=3), permutations(range(3), 3))
)

T = t.TypeVar("T")


def rotate(p: Point, rotation: Rotation) -> Point:
    return p[rotation[0]], p[rotation[1]], p[rotation[2]]


def unrotate(p: Point, rotation: Rotation) -> Point:
    inverse = [rotation.index(n) for n in range(3)]
    return p[inverse[0]], p[inverse[1]], p[inverse[2]]


def reorient_points(
    current_orientation: Orientation,
    new_orientation: Orientation,
    points: t.Sequence[Point],
) -> t.Sequence[Point]:
    for p in points:
        yield rotate(
            tuple(
                n * s * s2
                for n, s, s2 in zip(
                    unrotate(p, current_orientation.rotation),
                    current_orientation.signs,
                    new_orientation.signs,
                )
            ),
            new_orientation.rotation,
        )


class Scanner:
    def __init__(self, id_: int, beacons: t.Sequence[Point]):
        self.id = id_
        self.position: Option[Point] = None_()
        self.visible_beacons = beacons
        self.orientation: Option[Orientation] = None_()

    def __repr__(self):
        return (
            f"Scanner(id={self.id}, position={self.position!r}, "
            f"orientation={self.orientation!r})"
        )

    def commit_to_placement(self, position: Point, orientation: Orientation) -> None:
        assert self.position.replace(position).is_none()
        assert self.orientation.replace(orientation).is_none()
        self.visible_beacons = list(
            tuple(n + o for n, o in zip(p, position))
            for p in reorient_points(
                all_orientations[0], orientation, self.visible_beacons
            )
        )

    def try_determine_placement(self, other: Scanner) -> bool:
        assert self.orientation.is_none() and other.orientation.is_some()
        assert self.position.is_none() and other.position.is_some()

        # Find overlapping points
        for orientation in all_orientations:
            oriented_points = list(
                reorient_points(all_orientations[0], orientation, self.visible_beacons)
            )

            for point, other_point in product(
                oriented_points,
                other.visible_beacons,
            ):
                # Assume same beacon, subtract offset of scanner locations from
                # each own point and check if equal to other points

                #     a     b
                # S1.....P.....S2
                #  |___________|
                #      offset
                scanner_offset = tuple(a - b for a, b in zip(point, other_point))

                overlapping = set(other.visible_beacons) & set(
                    tuple(n - o for n, o in zip(p, scanner_offset))
                    for p in oriented_points
                )
                if len(overlapping) >= 12:
                    self.commit_to_placement(
                        tuple(map(op.neg, scanner_offset)),
                        orientation,
                    )
                    return True

        return False


scanners: list[Scanner] = []
for block in map(methodcaller("splitlines"), data.split("\n\n")):
    id_ = int(block[0].split(" ")[2])
    beacons = [tuple(map(int, l.split(","))) for l in block[1:]]
    scanners.append(Scanner(id_, beacons))

zero = scanners[0]
zero.position.replace((0, 0, 0))
zero.orientation.replace(all_orientations[0])


remaining_scanners = scanners.copy()
found_scanners = [remaining_scanners.pop(0)]

while remaining_scanners:
    for i, s in enumerate(remaining_scanners):
        found = False
        for s2 in found_scanners:
            if s.try_determine_placement(s2):
                found = True
                # print(s, s2)
                break

        if found:
            found_scanners.append(remaining_scanners.pop(i))
            print(len(found_scanners), "/", len(scanners))
            continue


print(len(set(b for s in found_scanners for b in s.visible_beacons)))


def distances():
    for s1, s2 in combinations(found_scanners, 2):
        yield sum(abs(a - b) for a, b in zip(s1.position.unwrap(), s2.position.unwrap()))


print(max(distances()))
