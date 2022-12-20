from aoc import *
import multiprocessing

TIME_LIMIT = 24


class Resources:
    __slots__ = "ore", "clay", "obsidian", "geode"

    def __init__(self, ore, clay, obsidian, geode):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode


blueprints = []
for line in data.splitlines():
    blueprint_id, raw_costs = line[len("Blueprint ") :].split(": ")
    costs = {}

    for cost in raw_costs.rstrip(".").split(". "):
        words = iter(cost.split(" "))
        assert next(words) == "Each"
        ty = next(words)
        assert next(words) == "robot"
        assert next(words) == "costs"

        deps = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        while True:
            amount = int(next(words))
            dep_ty = next(words)
            deps[dep_ty] = amount
            try:
                assert next(words) == "and"
            except StopIteration:
                break

        costs[ty] = Resources(**deps)

    blueprints.append((int(blueprint_id), costs))


def run(best_so_far, costs, minute, active_robots, stock, constructed_anything):
    if minute == TIME_LIMIT:
        score = stock.geode + active_robots.geode
        if score > best_so_far.cell_contents:
            best_so_far.cell_contents = score
        return score

    time_remaining = TIME_LIMIT - minute
    if best_so_far.cell_contents > stock.geode + active_robots.geode * (time_remaining + 1) + (time_remaining * (time_remaining - 1)) // 2:
        return 0

    in_construction = []
    cost = costs["geode"]
    if cost.ore <= stock.ore and cost.clay <= stock.clay and cost.obsidian <= stock.obsidian:
        in_construction.append("geode")
    else:
        prev_ore = stock.ore - active_robots.ore
        prev_clay = stock.clay - active_robots.clay
        for resource in ("obsidian", "clay", "ore"):
            cost = costs[resource]
            if cost.ore <= stock.ore and cost.clay <= stock.clay:
                if constructed_anything or prev_ore < cost.ore or prev_clay < cost.clay:
                    in_construction.append(resource)

    best = 0
    for new_resource in in_construction:
        cost = costs[new_resource]
        new_stock = Resources(
            stock.ore + active_robots.ore - cost.ore,
            stock.clay + active_robots.clay - cost.clay,
            stock.obsidian + active_robots.obsidian - cost.obsidian,
            stock.geode + active_robots.geode,
        )
        new_active_robots = Resources(
            active_robots.ore + (new_resource == "ore"),
            active_robots.clay + (new_resource == "clay"),
            active_robots.obsidian + (new_resource == "obsidian"),
            active_robots.geode + (new_resource == "geode"),
        )
        score = run(best_so_far, costs, minute + 1, new_active_robots, new_stock, True)
        if score > best:
            best = score

    new_stock = Resources(
        stock.ore + active_robots.ore,
        stock.clay + active_robots.clay,
        stock.obsidian + active_robots.obsidian,
        stock.geode + active_robots.geode,
    )
    score = run(best_so_far, costs, minute + 1, active_robots, new_stock, False)
    if score > best:
        best = score

    return best


class Cell:
    __slots__ = "cell_contents"


def thread(blueprint):
    id_, costs = blueprint
    cell = Cell()
    cell.cell_contents = 0
    best_score = run(cell, costs, 1, Resources(1, 0, 0, 0), Resources(0, 0, 0, 0), False)
    return id_ * best_score


with multiprocessing.Pool() as pool:
    print(sum(pool.map(thread, blueprints)))


def thread2(blueprint):
    _id, costs = blueprint
    cell = Cell()
    cell.cell_contents = 0
    best_score = run(cell, costs, 1, Resources(1, 0, 0, 0), Resources(0, 0, 0, 0), False)
    return best_score


TIME_LIMIT = 32

with multiprocessing.Pool() as pool:
    print(reduce(op.mul, pool.map(thread2, blueprints[:3])))
