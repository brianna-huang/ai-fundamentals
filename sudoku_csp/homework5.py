############################################################
# CIS 521: Homework 5
############################################################

import math
import random
import itertools
import copy
from collections import deque
student_name = "Brianna Huang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    cells = []
    for row in range(9):
        for col in range(9):
            cells.append((row, col))
    return cells


def sudoku_arcs():
    cells = sudoku_cells()
    arcs = set()

    # row and column constraints
    for row, col in cells:
        for other_col in range(9):
            if col != other_col:
                arcs.add(((row, col), (row, other_col)))
        for other_row in range(9):
            if row != other_row:
                arcs.add(((row, col), (other_row, col)))

    # sub-box constraint
    for sub_box_row in range(0, 9, 3):
        for sub_box_col in range(0, 9, 3):
            box_cells = [(r, c) for r in range(sub_box_row, sub_box_row + 3)
                         for c in range(sub_box_col, sub_box_col + 3)]
            for i in range(len(box_cells)):
                for j in range(i + 1, len(box_cells)):
                    arcs.add((box_cells[i], box_cells[j]))
                    arcs.add((box_cells[j], box_cells[i]))
    return arcs


def read_board(path):
    board_dict = {}
    values = set(range(1, 10))
    with open(path, 'r') as f:
        lines = [row.strip() for row in f.readlines()]
    board = [[col for col in row] for row in lines]
    for row in range(9):
        for col in range(9):
            if board[row][col] == '*':
                board_dict[(row, col)] = values
            else:
                board_dict[(row, col)] = {int(board[row][col])}
    return board_dict


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = dict(board)

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, xi, xj):
        xi_domain = self.get_values(xi)
        xj_domain = self.get_values(xj)

        if len(xj_domain) != 1:
            return False
        y = next(iter(xj_domain))

        to_remove = set([x for x in xi_domain if x == y])

        if len(to_remove) == 0:
            return False

        self.board[xi] = xi_domain - to_remove

        return True

    def neighbors(self, xi):
        neighbors = set()
        for (c1, c2) in Sudoku.ARCS:
            if xi == c1:
                neighbors.add(c2)
        return neighbors

    def infer_ac3(self):
        queue = deque(Sudoku.ARCS)
        while queue:
            (xi, xj) = queue.popleft()

            if self.remove_inconsistent_values(xi, xj):
                if len(self.get_values(xi)) == 0:
                    return False
                for xk in self.neighbors(xi) - {xj}:
                    queue.append((xk, xi))

        return True

    def add_inferred_value(self):
        inference = False
        for val in range(1, 10):
            row_poss = {r: [] for r in range(9)}
            col_poss = {c: [] for c in range(9)}
            box_poss = {(r, c): [] for r in range(3) for c in range(3)}
            # get possible cells for each digit
            for (row, col), values in self.board.items():
                if len(values) > 1 and val in values:
                    row_poss[row].append((row, col))
                    col_poss[col].append((row, col))
                    box_poss[(row // 3, col // 3)].append((row, col))
            for candidates in [row_poss, col_poss, box_poss]:
                for cells in candidates.values():
                    # if there is only 1 possibility for this value
                    if len(cells) == 1:
                        self.board[cells[0]] = {val}
                        inference = True
        return inference

    def infer_improved(self):
        extra_inference = True
        while extra_inference:
            self.infer_ac3()
            extra_inference = False
            if self.add_inferred_value():
                extra_inference = True

    def all_singles(self):
        if all(len(vals) == 1 for vals in self.board.values()):
            return True
        return False

    def infer_with_guessing(self):
        self.infer_improved()

        # all cells that have more than 1 possibility
        cells = [c for c in self.board.keys() if len(self.board[c]) > 1]
        for cell in cells:
            vals = list(self.board[cell])
            for val in vals:
                old_board = copy.deepcopy(self.board)
                self.board[cell] = {val}
                self.infer_with_guessing()

                if self.all_singles():
                    break
                else:
                    self.board = old_board
            return


############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
30
"""

feedback_question_2 = """
Wow this one was difficult. The most challenging aspects of this
assignment were implementing the infer_improved and
infer_with_guessing algorithms. Having to keep in mind the row,
column, and sub-box constraints was a lot to implement and keep
track of, and it was hard to fix some bugs that were placing
invalid values or not eliminating enough of them.
"""

feedback_question_3 = """
I love playing sudoku for fun, so implementing the algorithm for
it was really interesting. There were aspects in code where I'd
do a similar type of thinking when I'm doing the puzzles. Wouldn't
change anything.
"""
