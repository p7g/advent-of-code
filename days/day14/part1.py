from collections import defaultdict
from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()
    instrs = []

    for line in data:
        l, r = line.split(" = ")
        if l == "mask":
            r = r.replace("0", "a").replace("X", "0")
            or_ = r.replace("a", "0")
            and_ = r.replace("0", "1").replace("a", "0")
            instrs.append((l, (int(or_, 2), int(and_, 2))))
        else:
            l, addr = l.rstrip("]").split("[")
            instrs.append((r, (int(addr), int(r))))

    mask = (0, -1)
    mem = defaultdict(lambda: 0)
    for instr, args in instrs:
        if instr == "mask":
            mask = args
        else:
            addr, val = args
            mem[addr] = (val | mask[0]) & mask[1]

    print(sum(mem.values()))
