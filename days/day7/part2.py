from functools import partial
from itertools import permutations
from lib.intcode import IntCodeVM
from os import path
from .day7lib import fwd


def new_amp(code, phase_setting):
    vm = IntCodeVM.from_str(code)
    gen = vm.run()
    next(gen)
    gen.send(phase_setting)
    return gen


def run_phase_setting(code, setting):
    amps = map(partial(new_amp, code), setting)
    gen = fwd(amps)
    next(gen)
    return gen


def run_cycle(code, setting):
    gen = run_phase_setting(code, setting)
    try:
        v = gen.send(0)
        while True:
            next(gen)
            v = gen.send(v)
    except StopIteration:
        pass
    return v


if __name__ == "__main__":
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as f:
        code = f.read()

    namps = 5
    phase_settings = permutations(range(namps, 2 * namps), namps)
    print(max(map(partial(run_cycle, code), phase_settings)))
