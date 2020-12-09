from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()

    instrs = []
    for line in data:
        instr, n = line.split(" ")
        instrs.append((instr, int(n)))

    acc = 0
    ip = 0
    seen = set()

    while ip not in seen:
        seen.add(ip)
        i, n = instrs[ip]

        if i == "acc":
            acc += n
            ip += 1
        elif i == "jmp":
            ip += n
        elif i == "nop":
            ip += 1

    print(acc)
