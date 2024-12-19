from aoc import *

towels, designs = data.split("\n\n")
towels = towels.split(", ")
designs = designs.splitlines()

trie = {}
for towel in towels:
    current = trie
    for c in towel:
        current = current.setdefault(c, {})
    current["ok"] = True


def matches(design):
    current = trie
    prefix = ""
    for c in design:
        current = current.get(c)
        prefix += c
        if not current:
            break
        elif current.get("ok"):
            yield prefix


@cache
def npermutations(design):
    if not design:
        return 1
    result = 0
    for match in matches(design):
        result += npermutations(design.removeprefix(match))
    return result


s = 0
s2 = 0
for design in designs:
    n = npermutations(design)
    s += n != 0
    s2 += n
print(s)
print(s2)
