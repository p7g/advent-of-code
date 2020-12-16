from lib.input import fetch

if __name__ == "__main__":
    data = fetch(16)
    rules, _, nearby = data.strip().split("\n\n")
    rules = rules.splitlines()

    rs = []
    for rule in rules:
        f, opts = rule.split(": ")
        opts = [list(map(int, o.split("-"))) for o in opts.split(" or ")]
        rs.append((f, opts))
    rules = rs

    nearby = [list(map(int, l.split(","))) for l in nearby.splitlines()[1:]]

    s = 0
    for n in nearby:
        for fv in n:
            for _, opts in rules:
                if any(l <= fv <= h for l, h in opts):
                    break
            else:
                s += fv

    print(s)
