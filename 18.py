from aoc import *


class open_pair:
    pass


class close_pair:
    pass


def find_explodable(n):
    nesting = 0
    for i, p in enumerate(n):
        if p is open_pair:
            if nesting == 4:
                return i
            nesting += 1
        elif p is close_pair:
            nesting -= 1
    return None


def find_splitable(n):
    for i, p in enumerate(n):
        if isinstance(p, int) and p >= 10:
            return i
    return None


def reduce_(n):
    while True:
        i = find_explodable(n)
        if i is not None:
            l, r = n[i + 1 : i + 3]
            assert isinstance(l, int) and isinstance(r, int)
            for j in range(i, -1, -1):
                if isinstance(n[j], int):
                    n[j] += l
                    break
            for j in range(i + 4, len(n)):
                if isinstance(n[j], int):
                    n[j] += r
                    break
            n[i : i + 4] = [0]
            continue

        i = find_splitable(n)
        if i is not None:
            n[i : i + 1] = [open_pair, n[i] // 2, ceil(n[i] / 2), close_pair]
            continue

        break
    return n


def add_(a, b):
    return reduce_([open_pair, *a, *b, close_pair])


def parse(s):
    result = []
    num_acc = ""

    for c in s:
        if c == "[":
            result.append(open_pair)
        elif c == "]":
            if num_acc:
                result.append(int(num_acc))
                num_acc = ""
            result.append(close_pair)
        elif c == ",":
            if num_acc:
                result.append(int(num_acc))
                num_acc = ""
        else:
            num_acc += c

    return result


def magnitude(n):
    def _magnitude(n, pos=0):
        if n[pos] is open_pair:
            m, pos = _magnitude(n, pos + 1)
            m2, pos = _magnitude(n, pos)
            assert n[pos] == close_pair
            return 3 * m + 2 * m2, pos + 1
        else:
            assert isinstance(n[pos], int)
            return n[pos], pos + 1

    m, _ = _magnitude(n)
    return m


sum_ = reduce(add_, map(parse, data.splitlines()))
print(magnitude(sum_))


def magnitudes():
    for lines in combinations(data.splitlines(), 2):
        a, b = map(parse, lines)
        yield magnitude(add_(a, b))


print(max(magnitudes()))
