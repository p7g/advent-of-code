from lib import intcode
from os import path


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = list(map(int, f.read().strip().split(",")))

    vm = intcode.IntCodeVM(code)
    vm.memory[1:3] = 12, 2
    next(vm.run())

    print(vm.memory[0])
