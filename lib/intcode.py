import enum
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
    HALT = 99

    @property
    def nargs(self):
        if self in (self.ADD, self.MUL, self.LT, self.EQ):
            return 3
        if self in (self.JNZ, self.JZ):
            return 2
        if self in (self.INPUT, self.OUTPUT):
            return 1
        if self is self.HALT:
            return 0


class ParamMode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1


class IntCodeVM:
    _NOTHING = object()

    def __init__(self, code):
        self.memory = list(code)

    @classmethod
    def from_str(cls, code_raw):
        return cls(map(int, code_raw.strip().split(",")))

    def _parse_params(self, i, digits):
        digits = list(map(ParamMode, digits))
        digits.reverse()
        digits.extend([0] * (3 - len(digits)))

        def _getset_param(n, val=self._NOTHING):
            mode = ParamMode(digits[n - i - 1])
            if val is self._NOTHING:
                if mode is ParamMode.IMMEDIATE:
                    return self.memory[n]
                return self.memory[self.memory[n]]
            elif mode is ParamMode.POSITION:
                self.memory[self.memory[n]] = val
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
                param(i + 3, param(i + 1) + param(i + 2))
            elif opcode is Op.MUL:
                param(i + 3, param(i + 1) * param(i + 2))
            elif opcode is Op.INPUT:
                val = int((yield))
                out = mem[i + 1]
                mem[out] = val
            elif opcode is Op.OUTPUT:
                yield param(i + 1)
            elif opcode is Op.JNZ:
                if param(i + 1) != 0:
                    i = param(i + 2)
                    continue
            elif opcode is Op.JZ:
                if param(i + 1) == 0:
                    i = param(i + 2)
                    continue
            elif opcode is Op.LT:
                param(i + 3, int(param(i + 1) < param(i + 2)))
            elif opcode is Op.EQ:
                param(i + 3, int(param(i + 1) == param(i + 2)))
            else:
                raise NotImplementedError(opcode)

            i += opcode.nargs + 1
