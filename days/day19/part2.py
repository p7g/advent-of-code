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
        if rule_id == 0:
            m, rem = do_match(s, 42)
            if not m:
                return False, s
            m, rem2 = do_match(rem, 11)
            if m and not rem2:
                return True, ""
            return do_match(rem, 0)
        if rule_id == 11:
            rem = s
            m, rem = do_match(rem, 42)
            if not m:
                return False, s
            m, rem = do_match(rem, 11)
            m, rem = do_match(rem, 31)
            if m:
                return True, rem
            return False, s
        rule = rules[rule_id]
        if isinstance(rule, str):
            if s and s[0] == rule:
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
