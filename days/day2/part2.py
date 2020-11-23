from itertools import permutations
from lib import intcode
from os import path


def try_pair(code, pair):
    vm = intcode.IntCodeVM(code)
    vm.memory[1:3] = pair
    next(vm.run())
    return vm.memory[0]


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = list(map(int, f.read().strip().split(",")))

    for pair in permutations(range(len(code)), 2):
        if try_pair(code, pair) == 19690720:
            a, b = pair
            print(100 * a + b)
            break
    else:
        print("No solution")
