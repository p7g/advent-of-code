from aoc import *

cards = {}
for line in data.splitlines():
    card_id, rest = line.split(": ")
    card_id = int(card_id.split(" ", 1)[1])
    winning_numbers_txt, numbers_txt = rest.split(" | ", 1)
    winning_numbers = frozenset({int(x) for x in winning_numbers_txt.split(" ") if x})
    numbers = frozenset({int(x) for x in numbers_txt.split(" ") if x})
    cards[card_id] = (winning_numbers, numbers)

s = 0
for card_id, (winning_numbers, numbers) in cards.items():
    nmatches = len(winning_numbers & numbers)
    if nmatches == 0:
        continue
    s += 2 ** (nmatches - 1)

print(s)

num_cards = {card_id: 1 for card_id in cards}

for card_id, (winning_numbers, numbers) in cards.items():
    nmatches = len(winning_numbers & numbers)
    if nmatches == 0:
        continue
    for next_id in range(card_id + 1, card_id + 1 + nmatches):
        num_cards[next_id] += num_cards[card_id]

print(sum(num_cards.values()))
