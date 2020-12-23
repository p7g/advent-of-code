from itertools import count
from lib.input import fetch

if __name__ == "__main__":

    class node:
        __slots__ = "label", "next"

        def __init__(self, label):
            self.label = label
            self.next = None

    data = fetch().strip()
    all_cups = list(map(int, data))
    for i in range(max(all_cups) + 1, 1_000_000 + 1):
        all_cups.append(i)

    lookup = {}
    current = cups = lookup[all_cups[0]] = node(all_cups[0])
    for label in all_cups[1:]:
        cups.next = lookup[label] = node(label)
        cups = cups.next
    cups.next = current

    min_cup = min(all_cups)
    max_cup = max(all_cups)

    for move in count(1):
        a, b, c = current.next, current.next.next, current.next.next.next
        current.next = c.next

        dest = current.label - 1
        if dest < min_cup:
            dest = max_cup
        while dest == a.label or dest == b.label or dest == c.label:
            dest -= 1
            if dest < min_cup:
                dest = max_cup

        dest_node = lookup[dest]
        end = dest_node.next
        dest_node.next = a
        a.next = b
        b.next = c
        c.next = end

        current = current.next

        if move == 10_000_000:
            break

    one = lookup[1]
    print(one.next.label * one.next.next.label)
