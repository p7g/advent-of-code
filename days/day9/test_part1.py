from lib.intcode import IntCodeVM


def test_quine():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert list(IntCodeVM(code).run()) == code


def test_16digit_number():
    code = "1102,34915192,34915192,7,4,7,99,0"
    gen = IntCodeVM.from_str(code).run()
    assert len(str(next(gen))) == 16


def test_big_number():
    code = "104,1125899906842624,99"
    assert next(IntCodeVM.from_str(code).run()) == 1125899906842624


def test_adjust_relative_base():
    code = [109, 19, 204, -34, 99]
    vm = IntCodeVM(code)
    vm.relative_base = 2000
    vm.memory[1985] = 4321
    output = next(vm.run())
    assert vm.relative_base == 2019 and output == 4321
