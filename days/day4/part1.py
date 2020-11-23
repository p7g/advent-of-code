from .day4lib import (
    digits,
    has_6_digits,
    has_no_decreasing_digits,
    has_same_adjacent_digits,
)


def suitable(n):
    return (
        has_6_digits(n) and has_no_decreasing_digits(n) and has_same_adjacent_digits(n)
    )


if __name__ == "__main__":
    lower, upper = 130254, 678275
    print(sum(map(suitable, map(digits, range(lower, upper + 1)))))
