from lib.input import fetch

if __name__ == "__main__":
    data = fetch().strip()
    rules, messages = map(str.splitlines, data.split("\n\n"))

    rs = [None] * len(rules)
    for rule in rules:
        id_, spec = rule.split(": ")
        id_ = int(id_)

        if spec[0] == '"':
            c = spec[1]
            rs[id_] = c
        else:
            opts = spec.split(" | ")
            rs[id_] = [[int(n) for n in opt.split(" ")] for opt in opts]

    rules = rs

    def do_match(s, rule_id):
        rule = rules[rule_id]
        if isinstance(rule, str):
            if s[0] == rule:
                return True, s[1:]
            return False, s
        for alt in rule:
            rem = s
            for r in alt:
                matched, rem = do_match(rem, r)
                if not matched:
                    break
            else:
                return True, rem
        return False, s

    def matches(s, rule_id):
        m, rem = do_match(s, rule_id)
        return m and not rem

    print(sum(matches(msg, 0) for msg in messages))
