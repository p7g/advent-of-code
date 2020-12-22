from collections import deque
from lib.input import fetch

if __name__ == "__main__":
    data = fetch().strip()
    players = data.split("\n\n")

    def make_deck(p):
        _, *cards = p.splitlines()
        return deque(map(int, cards))

    p1, p2 = map(make_deck, players)

    while True:
        a, b = p1.popleft(), p2.popleft()
        assert a != b
        if a > b:
            w = p1
        elif a < b:
            w = p2

        w.append(max(a, b))
        w.append(min(a, b))

        if not p1 or not p2:
            break

    winner = p1 or p2
    score = 0
    for i, c in enumerate(reversed(winner)):
        score += c * (i + 1)

    print(score)
