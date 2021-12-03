from aoc import *

nums = data.splitlines()
gamma = ""
epsilon = ""

for i in range(len(nums[0])):
    ones = 0
    zeroes = 0
    for num in nums:
        if num[i] == '1':
            ones += 1
        elif num[i] == '0':
            zeroes += 1

    gamma += '1' if ones > zeroes else '0'
    epsilon += '1' if ones < zeroes else '0'

gamma = int(gamma, 2)
epsilon = int(epsilon, 2)

print(gamma * epsilon)


o_gen = nums
for i in range(len(o_gen[0])):
    c = Counter()
    for num in o_gen:
        c[num[i]] += 1
    z, o = c['0'], c['1']
    b = '1' if o >= z else '0'
    o_gen = [n for n in o_gen if n[i] == b]
    if len(o_gen) == 1:
        break

c_scrub = nums
for i in range(len(c_scrub[0])):
    c = Counter()
    for num in c_scrub:
        c[num[i]] += 1
    z, o = c['0'], c['1']
    b = '1' if o < z else '0'
    c_scrub = [n for n in c_scrub if n[i] == b]
    if len(c_scrub) == 1:
        break

print(int(o_gen[0], 2) * int(c_scrub[0], 2))
