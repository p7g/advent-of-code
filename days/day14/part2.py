from collections import defaultdict
from itertools import combinations
from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()
    instrs = []

    for line in data:
        l, r = line.split(" = ")
        if l == "mask":
            floating = []
            for i, c in enumerate(r):
                if c == "X":
                    floating.append(1 << (35 - i))
            and_ = int(r.replace("X", "0"), 2)
            instrs.append((l, (floating, and_)))
        else:
            l, addr = l.rstrip("]").split("[")
            instrs.append((r, (int(addr), int(r))))

    mask = ([], -1)
    mem = defaultdict(lambda: 0)
    for instr, args in instrs:
        if instr == "mask":
            mask = args
        else:
            floating, a = mask
            addr, val = args
            addr |= a
            m = 0
            for m_ in floating:
                m |= m_
            addr |= m
            mem[addr] = val
            for i in range(len(floating)):
                for c in combinations(floating, i + 1):
                    m2 = addr
                    for m_ in c:
                        m2 &= ~m_
                    mem[m2] = val

    print(sum(mem.values()))
