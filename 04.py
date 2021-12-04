from aoc import *

rnd, *board_text = data.split("\n\n")
rnd = list(map(int, rnd.split(",")))

boards = []
for txt in board_text:
    board = []
    for line in txt.splitlines():
        nums = list(map(int, re.split(r"\s+", line.strip())))
        board.append(nums)
    boards.append(board)


class Board:
    def __init__(self, board):
        self.board = board
        self.marked = set()
        self.won = None_()

    def mark(self, n):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col == n:
                    self.marked.add((x, y))

    def check_win(self, n):
        for y in range(len(self.board)):
            if all((x, y) in self.marked for x in range(len(self.board[0]))):
                self.won.replace(n)
                return True

        for x in range(len(self.board[0])):
            if all((x, y) in self.marked for y in range(len(self.board))):
                self.won.replace(n)
                return True

        return False

    def score(self):
        sum_unmarked = 0
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if (x, y) not in self.marked:
                    sum_unmarked += col
        return sum_unmarked * self.won.unwrap()


def part1():
    board_objs = list(map(Board, boards))

    for n in rnd:
        for i, board in enumerate(board_objs):
            board.mark(n)
            if board.check_win(n):
                print(i, board.score())
                return


part1()


def part2():
    board_objs = list(map(Board, boards))
    won = set()

    for n in rnd:
        for i, board in enumerate(board_objs):
            if i in won:
                continue
            board.mark(n)
            if board.check_win(n):
                won.add(i)
                print(i, board.score())


part2()
