from functools import partial
from itertools import permutations
from lib.intcode import IntCodeVM
from os import path
from .day7lib import one, fwd, pipe


def new_amp(code, phase_setting):
    vm = IntCodeVM.from_str(code)
    gen = vm.run()
    next(gen)
    gen.send(phase_setting)
    return gen


def run_phase_setting(code, setting):
    amps = fwd(map(partial(new_amp, code), setting))
    next(amps)
    result, = list(pipe(one(0), amps))
    return result


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = f.read()

    namps = 5
    phase_settings = permutations(range(namps), namps)

    print(max(map(partial(run_phase_setting, code), phase_settings)))
