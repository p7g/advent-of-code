from lib.input import fetch

if __name__ == "__main__":
    data = fetch(16)
    rules, mine, nearby = data.strip().split("\n\n")
    rules = rules.splitlines()

    rs = []
    for rule in rules:
        f, opts = rule.split(": ")
        opts = [list(map(int, o.split("-"))) for o in opts.split(" or ")]
        rs.append((f, opts))
    rules = rs

    nearby = [list(map(int, l.split(","))) for l in nearby.splitlines()[1:]]

    valid = []
    for ticket in nearby:
        for field in ticket:
            if not any(l <= field <= h for _, opts in rules for l, h in opts):
                break
        else:
            valid.append(ticket)

    fields = [None] * len(valid[0])
    while None in fields:
        for name, opts in rules:
            if name in fields:
                continue
            matched = []
            for col in range(len(valid[0])):
                if fields[col] is not None:
                    continue
                for ticket in valid:
                    if not any(l <= ticket[col] <= h for l, h in opts):
                        break
                else:
                    matched.append(col)
            if len(matched) == 1:
                fields[matched[0]] = name

    _, ticket = mine.strip().splitlines()
    ticket = list(map(int, ticket.split(",")))

    prod = 1
    for i, name in enumerate(fields):
        if name.startswith("departure"):
            prod *= ticket[i]

    print(prod)
