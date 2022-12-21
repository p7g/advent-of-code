from aoc import *


class Node:
    __slots__ = "value", "prev", "next"
    value: int
    prev: "Node"
    next: "Node"


start = end = None

for i in map(int, data.splitlines()):
    node = Node()
    node.value = i
    node.prev = end  # type: ignore
    if end is not None:
        end.next = node
    end = node
    node.next = None  # type: ignore
    if start is None:
        start = node

assert start and end

ordered_nodes = [start]
while ordered_nodes[-1].next:
    ordered_nodes.append(ordered_nodes[-1].next)

start.prev = end
end.next = start

for node in ordered_nodes:
    if node.value > 0:
        for _ in range(node.value):
            a, b, c = node.prev, node, node.next
            b.next = c.next
            b.next.prev = b
            b.prev = c
            c.next = b
            c.prev = a
            a.next = c
    elif node.value < 0:
        for _ in range(-node.value):
            a, b, c = node.prev, node, node.next
            b.prev = a.prev
            b.prev.next = b
            b.next = a
            a.prev = b
            a.next = c
            c.prev = a

zero = next(n for n in ordered_nodes if n.value == 0)

s = 0
cur = zero
for _ in range(1000):
    cur = cur.next
s += cur.value
for _ in range(1000):
    cur = cur.next
s += cur.value
for _ in range(1000):
    cur = cur.next
s += cur.value
print(s)


class Holder:
    __slots__ = ("x",)

    def __init__(self, x: int):
        self.x = x


numbers = [Holder(811589153 * int(l)) for l in data.splitlines()]
n_pos = {n: i for i, n in enumerate(numbers)}
pos_n = {i: n for i, n in enumerate(numbers)}

for _ in range(10):
    for n in numbers:
        if n.x == 0:
            continue
        current_pos = n_pos[n]
        new_pos = (current_pos + n.x) % (len(numbers) - 1)
        direction = sign(new_pos - current_pos)
        if direction == 0:
            continue
        for a, b in pairwise(range(current_pos, new_pos + direction, direction)):
            if a is None or b is None:
                continue
            pos_n[a] = pos_n[b]
            n_pos[pos_n[a]] = a
        pos_n[new_pos] = n
        n_pos[n] = new_pos

z = n_pos[next(n for n in numbers if n.x == 0)]
s = pos_n[(z + 1000) % len(numbers)].x
s += pos_n[(z + 2000) % len(numbers)].x
s += pos_n[(z + 3000) % len(numbers)].x
print(s)
