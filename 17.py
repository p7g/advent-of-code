from aoc import *

registers_text, program_text = data.split("\n\n")
A, B, C = (int(line.split(": ", 1)[1]) for line in registers_text.splitlines())
program = [int(n) for n in program_text.split(": ", 1)[1].split(",")]

adv, bxl, bst, jnz, bxc, out, bdv, cdv = range(8)


def computer(code, *, A, B, C):
    ip = 0

    def combo(operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            raise ValueError(operand)

    while ip < len(code):
        opcode, operand = code[ip:ip+2]

        if opcode == adv:
            A >>= combo(operand)
        elif opcode == bxl:
            B ^= operand
        elif opcode == bst:
            B = combo(operand) & 7
        elif opcode == jnz:
            if A != 0:
                ip = operand
                continue
        elif opcode == bxc:
            B ^= C
        elif opcode == out:
            yield combo(operand) & 7
        elif opcode == bdv:
            B = A >> combo(operand)
        elif opcode == cdv:
            C = A >> combo(operand)
        else:
            raise ValueError(opcode)

        ip += 2


print(",".join(map(str, computer(program, A=A, B=B, C=C))))

answers = [0]
for n in reversed(program):
    possible_solutions = []
    for answer in answers:
        for i in range(8):
            A = (answer << 3) + i
            result = next(computer(program, A=A, B=0, C=0))
            if result == n:
                possible_solutions.append(A)
    if not possible_solutions:
        raise Exception("no solution")
    answers = possible_solutions

print(min(answers))
