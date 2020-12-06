from math import ceil, floor


def get_id(line):
    line = line.strip()

    lower, upper = 0, 127
    for c in line[:7]:
        if c == 'F':
            upper = floor((lower + upper) / 2)
        elif c == 'B':
            lower = ceil((lower + upper) / 2)
    assert lower == upper
    y = lower

    lower, upper = 0, 7
    for c in line[7:]:
        if c == 'L':
            upper = floor((lower + upper) / 2)
        elif c == 'R':
            lower = ceil((lower + upper) / 2)
    assert lower == upper
    x = upper
    return (y * 8 + x)
