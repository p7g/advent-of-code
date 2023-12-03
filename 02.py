from aoc import *

games = {}
for line in data.splitlines():
    game_id, hands = line.split(": ")
    game = games[int(game_id.split(" ", 1)[1])] = []
    for hand_text in hands.split("; "):
        hand = {}
        game.append(hand)
        for colour in hand_text.split(", "):
            count, colour = colour.split(" ", 1)
            hand[colour] = int(count)


num_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
s = 0
for game_id, game in games.items():
    for hand in game:
        for colour, count in hand.items():
            if count > num_cubes[colour]:
                break
        else:
            continue
        break
    else:
        s += game_id

print(s)


power_sum = 0
for game in games.values():
    min_cubes = defaultdict(int)
    for hand in game:
        for colour, count in hand.items():
            if count > min_cubes[colour]:
                min_cubes[colour] = count
    power = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    power_sum += power

print(power_sum)
