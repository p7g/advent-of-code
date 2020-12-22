from collections import deque
from lib.input import fetch

if __name__ == "__main__":
    data = fetch().strip()
    players = data.split("\n\n")

    def make_deck(p):
        _, *cards = p.splitlines()
        return deque(map(int, cards))

    def snapshot(*players):
        return tuple(map(tuple, players))

    def game(p1, p2):
        past_states = set()
        while True:
            if snapshot(p1, p2) in past_states:
                return p1
            past_states.add(snapshot(p1, p2))

            a, b = p1.popleft(), p2.popleft()
            if len(p1) >= a and len(p2) >= b:
                p12, p22 = deque(list(p1)[:a]), deque(list(p2)[:b])
                w2 = game(p12, p22)
                w = p1 if w2 is p12 else p2
                c = a if w is p1 else b
            else:
                w, c = (p1, a) if a > b else (p2, b)

            w.append(c)
            w.append(a if b == c else b)

            if not p1 or not p2:
                return p1 or p2

    p1, p2 = map(make_deck, players)
    score = 0

    for i, c in enumerate(reversed(game(p1, p2))):
        score += c * (i + 1)

    print(score)
