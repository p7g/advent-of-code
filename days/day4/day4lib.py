from lib.digits import digits


def has_6_digits(n):
    return len(n) == 6


def has_no_decreasing_digits(n):
    current, *digs = n
    for dig in digs:
        if dig < current:
            return False
        current = dig
    return True


def has_same_adjacent_digits(n):
    current, *digs = n
    for n in digs:
        if n == current:
            return True
        current = n
    return False


def has_2_same_adjacent_digits(digs):
    current, *digs = digs
    streak = 0
    for dig in digs:
        if dig == current:
            streak += 1
        elif streak == 1:
            return True
        else:
            streak = 0
        current = dig
    return streak == 1
