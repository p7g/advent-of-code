from lib.input import get_input_lines


def part2(data):
    data = list(map(int, map(str.strip, data)))
    for a in data:
        for b in data:
            for c in data:
                if a + b + c == 2020:
                    return a * b * c


if __name__ == "__main__":
    print(part2(get_input_lines()))
