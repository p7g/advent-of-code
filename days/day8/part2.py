from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()

    instrs = []
    for line in data:
        instr, n = line.split(" ")
        instrs.append((instr, int(n)))

    acc = 0
    ip = 0

    for i, (inst, n) in enumerate(instrs):
        if inst == "nop":
            if n == 0:
                continue
            copy = instrs.copy()
            copy[i] = "jmp", n
        elif inst == "jmp":
            copy = instrs.copy()
            copy[i] = "nop", n
        else:
            continue

        acc = 0
        ip = 0
        seen = set()

        while True:
            if ip >= len(copy):
                break
            elif ip in seen:
                break

            seen.add(ip)
            i, n = copy[ip]

            if i == "acc":
                acc += n
                ip += 1
            elif i == "jmp":
                ip += n
            elif i == "nop":
                ip += 1

        if ip == len(copy):
            print(acc)
            break
