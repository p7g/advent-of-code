from functools import reduce
from operator import mul
from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines(18)

    def atom(s):
        global pos
        if s[pos] == "(":
            pos += 1
            v = parse(s)
            pos += 1  # )
            return v

        n = ""
        while pos < len(s) and s[pos].isdigit():
            n += s[pos]
            pos += 1

        return int(n)

    def parse(s):
        global pos
        stack = [atom(s)]

        while pos < len(s) and s[pos] != ")":
            op = s[pos]
            pos += 1
            if op == " ":
                continue
            assert op in ("+", "*"), op

            pos += 1
            r = atom(s)
            stack.append(r)

            if op == "+":
                stack.append(stack.pop() + stack.pop())

        return reduce(mul, stack)

    s = 0
    for line in data:
        line = line.strip()
        pos = 0
        s += parse(line)

    print(s)
