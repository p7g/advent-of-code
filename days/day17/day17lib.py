import enum
import networkx as nx


class Tile(enum.Enum):
    space = "."
    scaffolding = "#"
    robot_up = "^"
    robot_down = "v"
    robot_left = "<"
    robot_right = ">"
    robot_tumbling = "X"


def read_from_vm(vm):
    text = ""
    try:
        while True:
            val = next(vm)
            if not val:
                return text
            text += chr(val)
    except StopIteration:
        return text


def tail(vm):
    line = ""
    while True:
        try:
            val = next(vm)
            if val > 128:
                return val
            line += chr(val)
        except StopIteration:
            break
        finally:
            if line and line[-1] == "\n":
                print(line, end="")
                line = ""


def send_line(vm, line):
    for c in line:
        v = vm.send(ord(c))
        if v is not None:
            print(chr(v), end="")
    print(chr(vm.send(ord("\n"))), end="")


def text_to_tiles(text):
    return [list(map(Tile, ts.strip())) for ts in text.strip().splitlines()]


def make_grid(tiles):
    w, h = len(tiles[0]), len(tiles)
    G = nx.grid_2d_graph(w, h)

    for y, row in enumerate(tiles):
        for x, type_ in enumerate(row):
            G.add_node((x, y), type=type_)

    return G
