from aoc import *


def nbrs_and_self(x, y):
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


enhancement_alg, image = data.split("\n\n")
image = [list(line) for line in image.splitlines()]

output_image = {}

for y, row in enumerate(image):
    for x, c in enumerate(row):
        output_image[x, y] = c == "#"


infinite_value = False

for i in count(1):
    new_image = {}

    for x, y in output_image.keys():
        nbrs = nbrs_and_self(x, y)

        for p in nbrs:
            bits = []
            for p2 in nbrs_and_self(*p):
                bits.append(output_image.get(p2, infinite_value))
            idx = int("".join(str(int(b)) for b in bits), 2)
            is_now_lit = enhancement_alg[idx] == "#"
            if p in new_image:
                assert new_image[p] == is_now_lit
            new_image[p] = is_now_lit

    infinite_value = "#" == enhancement_alg[-1 if infinite_value else 0]
    output_image = new_image

    if i in (2, 50):
        assert not infinite_value
        print(sum(v for v in output_image.values()))
        if i == 50:
            break
