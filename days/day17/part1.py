from lib.intcode import IntCodeVM
from lib.input import get_input
from .day17lib import read_from_vm, text_to_tiles, Tile, make_grid


def part1(text):
    G = make_grid(text_to_tiles(text))

    s = 0
    for node in G:
        if G.nodes[node]["type"] is not Tile.scaffolding or len(G[node]) < 4:
            continue
        is_intersection = True
        for nbr in G[node]:
            if G.nodes[nbr]["type"] is not Tile.scaffolding:
                is_intersection = False
                break
        if is_intersection:
            x, y = node
            s += x * y

    return s


if __name__ == "__main__":
    vm = IntCodeVM.from_str(get_input()).run()

    print(part1(read_from_vm(vm)))
