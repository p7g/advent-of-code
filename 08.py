from aoc import *

s = 0

for hints, code in map(methodcaller("split", " | "), data.splitlines()):
    code = code.split(" ")

    for num in code:
        if len(num) in [2, 3, 4, 7]:
            s += 1

print(s)

mapping = {2: 1, 3: 7, 4: 4, 7: 8}
s = 0

for hints, code in map(methodcaller("split", " | "), data.splitlines()):
    hints = hints.split(" ")
    code = code.split(" ")

    for hint in hints:
        if len(hint) == 2:
            one = set(hint)
        elif len(hint) == 3:
            seven = set(hint)
        elif len(hint) == 4:
            four = set(hint)
        elif len(hint) == 7:
            eight = set(hint)

    digits = ""

    for num in code:
        if len(num) in mapping:
            digits += str(mapping[len(num)])
        elif len(num) == 6:
            if ((set(num) & four) == four):
                digits += ("9")
            elif ((set(num) & seven) == seven):
                digits += ("0")
            else:
                digits += ("6")
        elif len(num) == 5:
            if (set(num) & seven) == seven:
                digits += ("3")
            elif len(set(num) & four) == 3:
                digits += ("5")
            else:
                digits += ("2")

    s += int(digits)

print(s)
