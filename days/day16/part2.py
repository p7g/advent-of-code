from lib.input import get_input
from .day16lib import read_input


def part2(input_):
    data = read_input(input_, 10_000)
    msg_offset = int(input_[:7])
    rem_len = len(data) - msg_offset

    # I'm not smart enough to come up with this myself; credit:
    # https://work.njae.me.uk/2019/12/20/advent-of-code-2019-day-16/
    current = data[msg_offset:]
    for _step in range(100):
        new = [0] * rem_len
        for i in reversed(range(rem_len)):
            if i == rem_len - 1:
                new[i] = current[i]
            else:
                new[i] = (new[i + 1] + current[i]) % 10
        current = new

    return current[:8]


if __name__ == "__main__":
    print(part2(get_input().strip()))
