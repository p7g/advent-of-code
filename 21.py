from aoc import *

die = cycle(range(1, 101))
players = [(0, int(line.rsplit(" ")[-1])) for line in data.splitlines()]

for turn in count(1):
    score, pos = players[(turn + 1) % 2]

    pos += sum(islice(die, 0, 3))
    pos = (pos % 10) or 10
    score += pos

    players[(turn + 1) % 2] = (score, pos)

    if score >= 1000:
        print(min(s for s, _ in players) * turn * 3)
        break

State = namedtuple("State", "turn,nrolls,roll,p1pos,p1score,p2pos,p2score")

p1pos, p2pos = [int(line.rsplit(" ")[-1]) for line in data.splitlines()]
states = defaultdict(
    int,
    {
        State(0, 0, 0, p1pos, 0, p2pos, 0): 1,
    },
)

wins = [0, 0]

while states:
    new_states = defaultdict(int)
    for (turn, nrolls, roll, p1pos, p1score, p2pos, p2score), ntimes in states.items():
        if nrolls == 3:
            pos, score = (p1pos, p1score) if turn == 0 else (p2pos, p2score)
            pos = ((pos + roll) % 10) or 10
            score += pos
            if score >= 21:
                wins[turn] += ntimes
                continue
            if turn == 0:
                p1pos = pos
                p1score = score
            else:
                p2pos = pos
                p2score = score
            new_states[State((turn + 1) % 2, 0, 0, p1pos, p1score, p2pos, p2score)] += ntimes
        else:
            for i in range(1, 4):
                new_states[
                    State(turn, nrolls + 1, roll + i, p1pos, p1score, p2pos, p2score)
                ] += ntimes
    states = new_states

print(max(wins))
