from lib.input import get_input_lines


def part1(data):
    data = list(map(int, map(str.strip, data)))
    for a in data:
        for b in data:
            if a + b == 2020:
                return a * b


if __name__ == "__main__":
    print(part1(get_input_lines()))
