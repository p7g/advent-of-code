import keyword
import operator
from aoc import *
import networkx as nx

workflows, parts = data.split("\n\n")

for workflow in workflows.splitlines():
    name, steps = workflow.removesuffix("}").split("{", 1)

    code_steps = []
    for step in steps.split(","):
        if ":" not in step:
            step = f"{step}_" if keyword.iskeyword(step) else step
            code = f"\treturn {step}(x, m, a, s)"
        else:
            cond, dest = step.split(":", 1)
            dest = f"{dest}_" if keyword.iskeyword(dest) else dest
            code = f"\tif {cond}: return {dest}(x, m, a, s)"
        code_steps.append(code)

    name = f"{name}_" if keyword.iskeyword(name) else name
    code = "\n".join([f"def {name}(x, m, a, s):", *code_steps])
    exec(code, globals())

sol = 0


def A(x, m, a, s):
    global sol
    sol += x + m + a + s


def R(*args):
    return


for part in parts.splitlines():
    part = eval(part.replace("{", '{"').replace("=", '": ').replace(",", ',"'))
    in_(**part)

print(sol)


workflows_by_name = {}
for workflow in workflows.splitlines():
    name, steps = workflow.removesuffix("}").split("{", 1)

    real_steps = []
    for step in steps.split(","):
        if ":" in step:
            step, dest = step.split(":", 1)
            if "<" in step:
                op = "<"
                var, amount = step.split("<", 1)
            else:
                assert ">" in step
                op = ">"
                var, amount = step.split(">", 1)
            real_steps.append((var, op, int(amount), dest))
        else:
            real_steps.append(step)

    workflows_by_name[name] = real_steps


def remove_range(ranges, range_):
    lo, hi = range_
    new_ranges = []
    for lo2, hi2 in ranges:
        if lo <= lo2 <= hi < hi2:
            new_ranges.append((hi + 1, hi2))
        elif lo <= lo2 < hi2 <= hi:
            continue
        elif lo2 < lo <= hi2 <= hi:
            new_ranges.append((lo2, lo - 1))
        elif lo2 < lo <= hi < hi2:
            new_ranges.extend([(lo2, lo - 1), (hi + 1, hi2)])
        elif lo == lo2 and hi == hi2:
            continue
        else:
            new_ranges.append((lo2, hi2))
    return new_ranges


def go(name, constraints):
    if name == "A":
        return reduce(
            operator.mul,
            (sum(hi - lo + 1 for lo, hi in ranges) for ranges in constraints.values()),
        )
    elif name == "R":
        return 0

    result = 0
    for step in workflows_by_name[name]:
        if isinstance(step, str):
            result += go(step, constraints)
        else:
            var, op, limit, dest = step
            new_constraints = constraints.copy()
            if op == "<":
                new_constraints[var] = remove_range(new_constraints[var], (limit, 4000))
                constraints[var] = remove_range(constraints[var], (1, limit - 1))
            else:
                assert op == ">"
                new_constraints[var] = remove_range(new_constraints[var], (1, limit))
                constraints[var] = remove_range(constraints[var], (limit + 1, 4000))
            result += go(dest, new_constraints)

    return result


print(go("in", {var: [(1, 4000)] for var in "xmas"}))
