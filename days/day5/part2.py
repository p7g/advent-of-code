from lib.intcode import IntCodeVM
from os import path


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code_raw = f.read()

    vm = IntCodeVM.from_str(code_raw).run()
    next(vm)
    print(vm.send(5))
