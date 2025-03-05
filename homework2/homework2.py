############################################################
# CIS 521: Homework 2
############################################################

from collections import deque
import random
from math import comb, factorial
student_name = "Brianna Huang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    return comb(n**2, n)


def num_placements_one_per_row(n):
    return n**n


def n_queens_valid(board):
    n = len(board)
    for queen1 in range(n):
        for queen2 in range(queen1+1, n):
            if (board[queen1] == board[queen2] or
                    abs(board[queen1]-board[queen2]) == abs(queen1-queen2)):
                return False
    return True


def n_queens_helper(n, board, valid):
    if len(board) == n:
        valid.append(board)
    else:
        # iterate through all possibilities for the next queen
        for queen in range(n):
            no_diag = True
            for ind, other_q in enumerate(board):
                if abs(queen-other_q) == len(board) - ind:
                    no_diag = False
            if queen not in board and no_diag:
                n_queens_helper(n, board+[queen], valid)


def n_queens_solutions(n):
    solutions = []
    n_queens_helper(n, [], solutions)
    return solutions


############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = list(board)
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        cells = [(row-1, col), (row+1, col), (row, col+1), (row, col-1)]
        for r, c in cells:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in self.board:
            for col in row:
                if col:
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle([col for col in row] for row in self.board)

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                new_board = self.copy()
                new_board.perform_move(row, col)
                yield (row, col), new_board

    def find_solution(self):
        frontier = [(self.board, [])]
        board = tuple(tuple(row) for row in self.board)
        visited = set(board)
        while len(frontier) > 0:
            curr, steps = frontier.pop(0)
            curr = LightsOutPuzzle(curr)
            if curr.is_solved():
                return steps
            for (row, col), new_board in curr.successors():
                visiting = tuple(tuple(r) for r in new_board.board)
                if visiting not in visited:
                    frontier.append((new_board.board, steps+[(row, col)]))
                    visited.add(visiting)
        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([False for _ in range(cols)] for _ in range(rows))

############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_identical_disks(length, n):
    start = tuple(range(n))
    end = tuple(range(length-n, length))
    frontier = [(start, [])]
    visited = set([start])

    while len(frontier) > 0:
        curr, steps = frontier.pop(0)
        if sorted(curr) == sorted(end):
            return steps
        for i in range(n):
            if curr[i] + 1 < length and curr[i] + 1 not in curr:
                visiting = list(curr)
                visiting[i] = visiting[i] + 1
                visiting = tuple(visiting)
                if visiting not in visited:
                    new_steps = steps + [(curr[i], curr[i]+1)]
                    frontier.append((visiting, new_steps))
                    visited.add(visiting)
            if (curr[i] + 2 < length and curr[i] + 2 not in curr
                    and curr[i] + 1 in curr):
                visiting = list(curr)
                visiting[i] = visiting[i] + 2
                visiting = tuple(visiting)
                if visiting not in visited:
                    new_steps = steps + [(curr[i], curr[i]+2)]
                    frontier.append((visiting, new_steps))
                    visited.add(visiting)
    return []


def solve_distinct_disks(length, n):
    start = tuple(range(n))
    end = tuple(range(length-1, length - n - 1, -1))
    frontier = [(start, [])]
    visited = set([start])

    while len(frontier) > 0:
        curr, steps = frontier.pop(0)
        if curr == end:
            return steps
        for i in range(n):
            if curr[i] + 1 < length and curr[i] + 1 not in curr:
                visiting = list(curr)
                visiting[i] = visiting[i] + 1
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.append((visiting, steps + [(curr[i], curr[i]+1)]))
                    visited.add(visiting)
            if (curr[i] + 2 < length and curr[i] + 2 not in curr
                    and curr[i] + 1 in curr):
                visiting = list(curr)
                visiting[i] = visiting[i] + 2
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.append((visiting, steps + [(curr[i], curr[i]+2)]))
                    visited.add(visiting)
            if curr[i] - 1 >= 0 and curr[i] - 1 not in curr:
                visiting = list(curr)
                visiting[i] = visiting[i] - 1
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.append((visiting, steps + [(curr[i], curr[i]-1)]))
                    visited.add(visiting)
            if (curr[i] - 2 >= 0 and curr[i] - 2 not in curr
                    and curr[i] - 1 in curr):
                visiting = list(curr)
                visiting[i] = visiting[i] - 2
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.append((visiting, steps + [(curr[i], curr[i]-2)]))
                    visited.add(visiting)
    return []


############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
10
"""

feedback_question_2 = """
The BFS implementation of the Linear Disk problem was definitely the
hardest for me. It was difficult to keep track of the different
visited/frontier grid states and the moves of this game to be
consistent with the properties of the BFS algorithm, so that it
would reliably get the shortest path each time.
"""

feedback_question_3 = """
Testing out and playing the games in the GUI is always fun.
I really like the format of the N-queens problem and Lights Out problem,
where it was broken up into many smaller helper functions at first.
It made it much more digestible and not as daunting as I thought it
would be. Wouldn't change anything.
"""
