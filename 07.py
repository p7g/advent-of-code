from aoc import *

data2 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()

card_strength = {card: strength for strength, card in enumerate("23456789TJQKA")}
hands, bids = zip(*(tuple(line.split(None, 1)) for line in data.splitlines()))
bids = tuple(int(bid) for bid in bids)
bids_by_hand = dict(zip(hands, bids))


def key(hand):
    counts = Counter(hand)
    most_common_card_count = counts.most_common(1)[0][1]

    if len(counts) == 5:
        hand_strength = 0
    elif len(counts) == 4:
        hand_strength = 1
    elif len(counts) == 3:
        if most_common_card_count == 2:
            hand_strength = 2
        else:
            hand_strength = 3
    elif len(counts) == 2:
        if most_common_card_count == 3:
            hand_strength = 4
        else:
            assert most_common_card_count == 4
            hand_strength = 5
    else:
        assert len(counts) == 1
        hand_strength = 6

    return hand_strength, *(card_strength[card] for card in hand)


sorted_hands = sorted(hands, key=key)
print(sum(bids_by_hand[hand] * rank for rank, hand in enumerate(sorted_hands, 1)))

card_strength = {card: strength for strength, card in enumerate("J23456789TQKA")}


def key(hand):
    counts = Counter(hand)
    num_jokers = counts.pop("J", 0)
    cards_by_count = counts.most_common()

    if not cards_by_count:
        counts["A"] += num_jokers
    elif len(cards_by_count) == 1:
        pass
    elif cards_by_count[0][1] != cards_by_count[1][1]:
        counts[cards_by_count[0][0]] += num_jokers
    else:
        options = sorted(
            [card for card, count in cards_by_count if count == cards_by_count[0][1]],
            key=card_strength.__getitem__,
        )
        counts[options[-1]] += num_jokers

    most_common_card_count = counts.most_common(1)[0][1]

    if len(counts) == 5:
        hand_strength = 0
    elif len(counts) == 4:
        hand_strength = 1
    elif len(counts) == 3:
        if most_common_card_count == 2:
            hand_strength = 2
        else:
            hand_strength = 3
    elif len(counts) == 2:
        if most_common_card_count == 3:
            hand_strength = 4
        else:
            assert most_common_card_count == 4, repr(counts)
            hand_strength = 5
    else:
        assert len(counts) == 1
        hand_strength = 6

    return hand_strength, *(card_strength[card] for card in hand)


sorted_hands = sorted(hands, key=key)
print(sum(bids_by_hand[hand] * rank for rank, hand in enumerate(sorted_hands, 1)))
