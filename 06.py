from aoc import *

data2 = "3,4,3,1,2"


fishes = list(map(int, data.split(",")))

for tick in count(1):
    for i in range(len(fishes)):
        if fishes[i] == 0:
            fishes[i] = 6
            fishes.append(8)
        else:
            fishes[i] -= 1
    if tick == 80:
        print(len(fishes))
        break


# Idea stolen from https://github.com/cpmsmith/advent-of-node-2020

fishes_by_days = Counter()
for days in data.split(","):
    fishes_by_days[int(days)] += 1

for tick in count(1):
    for i in range(0, 9):
        fishes_by_days[i - 1] += fishes_by_days[i]
        fishes_by_days[i] = 0

    fishes_by_days[8] = fishes_by_days[-1]
    fishes_by_days[6] += fishes_by_days[-1]
    fishes_by_days[-1] = 0

    if tick == 256:
        print(sum(fishes_by_days.values()))
        break
