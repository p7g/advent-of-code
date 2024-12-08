from aoc import *

eqs = []
for line in data.splitlines():
    result_str, operands_str = line.split(": ")
    eqs.append((int(result_str), [int(operand) for operand in operands_str.split()]))


def run(operators):
    s = 0
    for expected_result, operands in eqs:
        for ops in product(operators, repeat=len(operands) - 1):
            ops = iter(ops)
            result = reduce(lambda acc, operand: next(ops)(acc, operand), operands)
            if result == expected_result:
                s += result
                break
    return s


print(run([op.add, op.mul]))


def concat_operator(l, r):
    return l * (10 ** (int(log10(r)) + 1)) + r


print(run([op.add, op.mul, concat_operator]))
