import enum
from collections import ChainMap, defaultdict
from .digits import digits, undigits


class Op(enum.Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JNZ = 5
    JZ = 6
    LT = 7
    EQ = 8
    ADJREL = 9
    HALT = 99

    @property
    def nargs(self):
        if self in (self.ADD, self.MUL, self.LT, self.EQ):
            return 3
        if self in (self.JNZ, self.JZ):
            return 2
        if self in (self.INPUT, self.OUTPUT, self.ADJREL):
            return 1
        if self is self.HALT:
            return 0


class ParamMode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class IntCodeVM:
    _NOTHING = object()

    def __init__(self, code):
        self.memory = ChainMap(dict(enumerate(code)), defaultdict(lambda: 0))
        self.relative_base = 0

    @classmethod
    def from_str(cls, code_raw):
        return cls(map(int, code_raw.strip().split(",")))

    def _parse_params(self, i, digits):
        digits = list(map(ParamMode, digits))
        digits.reverse()
        digits.extend([0] * (3 - len(digits)))

        def _getset_param(n, val=self._NOTHING):
            mode = ParamMode(digits[n])
            idx = self.memory[i + n + 1]
            if val is self._NOTHING:
                if mode is ParamMode.IMMEDIATE:
                    return idx
                elif mode is ParamMode.POSITION:
                    return self.memory[idx]
                return self.memory[self.relative_base + idx]
            elif mode is ParamMode.POSITION:
                self.memory[idx] = val
            elif mode is ParamMode.RELATIVE:
                self.memory[self.relative_base + idx] = val
            else:
                raise ValueError("Can't set immediate param")

        return _getset_param

    def run(self):
        mem = self.memory
        i = 0

        while i < len(mem):
            instr = digits(mem[i])
            opcode = Op(undigits(instr[-2:]))
            param = self._parse_params(i, instr[:-2])

            if opcode is Op.HALT:
                break
            elif opcode is Op.ADD:
                param(2, param(0) + param(1))
            elif opcode is Op.MUL:
                param(2, param(0) * param(1))
            elif opcode is Op.INPUT:
                val = int((yield))
                param(0, val)
            elif opcode is Op.OUTPUT:
                yield param(0)
            elif opcode is Op.JNZ:
                if param(0) != 0:
                    i = param(1)
                    continue
            elif opcode is Op.JZ:
                if param(0) == 0:
                    i = param(1)
                    continue
            elif opcode is Op.LT:
                param(2, int(param(0) < param(1)))
            elif opcode is Op.EQ:
                param(2, int(param(0) == param(1)))
            elif opcode is Op.ADJREL:
                self.relative_base += param(0)
            else:
                raise NotImplementedError(opcode)

            i += opcode.nargs + 1
