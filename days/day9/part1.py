import sys
from lib.intcode import IntCodeVM
from os import path


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = f.read()

    gen = IntCodeVM.from_str(code).run()
    next(gen)
    output = [gen.send(1)]
    output.extend(gen)

    if output[1:]:
        print(output, file=sys.stderr)
        sys.exit(1)

    print(output[0])
