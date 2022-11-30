# Advent of code solutions

This branch has solutions for 2022, for other years see the other branches:

- [2021](https://github.com/p7g/advent-of-code-2020/tree/2021)
- [2020](https://github.com/p7g/advent-of-code-2020/tree/2020)
- [2019](https://github.com/p7g/advent-of-code-2020/tree/2019)

## Instructions if you wanna use aoc.py

1. Set up a Python virtual environment and install the dependencies with `python -m pip install -r requirements.txt`
2. Grab the cookie named "session" from adventofcode.com after you've signed in and put that in a file called .aoc-session
3. Name your solution files like 01.py (zero-padded to 2 digits)
4. Optionally `from aoc import *` in your solutions to import the prelude
5. Either run the solutions directly (i.e. `python 01.py`) or just run `./aoc.py` and it will run today's solution

The input for the problem (a str) can be found in the `data` member of the `aoc` module. The input is cached so it's only requested once per day.

To manually specify which solution to run and the input to use, use the `AOC_YEAR` and `AOC_DAY` environment variables.
