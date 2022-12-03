from aoc import *
import string

bags = [(s[:len(s)//2], s[len(s)//2:]) for s in data.splitlines()]
priority = dict(zip(chain(string.ascii_lowercase, string.ascii_uppercase), count(1)))

print(sum(priority[next(iter((set(a) & set(b))))] for a, b in bags))

print(sum(priority[next(iter(set.intersection(*map(set, chunk))))] for chunk in it.chunked(data.splitlines(), 3)))
