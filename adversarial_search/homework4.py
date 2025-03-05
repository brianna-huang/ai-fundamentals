############################################################
# CIS 521: Homework 4
############################################################

import math
import random
import itertools
import copy
import collections
student_name = "Brianna Huang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    return DominoesGame([[False for _ in range(cols)] for _ in range(rows)])


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = list(board)
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for _ in range(self.cols)]
                      for _ in range(self.rows)]

    def is_legal_move(self, row, col, vertical):
        if (vertical and row+1 < self.rows
                and not self.board[row][col] and not self.board[row+1][col]):
            return True
        if (not vertical and col+1 < self.cols
                and not self.board[row][col] and not self.board[row][col+1]):
            return True
        return False

    def legal_moves(self, vertical):
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_legal_move(row, col, vertical):
                    moves.append((row, col))
        return moves

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row+1][col] = True
        else:
            self.board[row][col+1] = True

    def game_over(self, vertical):
        if len(self.legal_moves(vertical)) == 0:
            return True
        return False

    def copy(self):
        return DominoesGame([row[:] for row in self.board])

    def successors(self, vertical):
        for row, col in self.legal_moves(vertical):
            new_board = self.copy()
            new_board.perform_move(row, col, vertical)
            yield ((row, col), new_board)

    def get_random_move(self, vertical):
        return random.choice(self.legal_moves(vertical))

    def utility(self, vertical, curr_player):
        current = len(self.legal_moves(vertical))
        opponent = len(self.legal_moves(not vertical))
        # if we want utility from the point of view of the current player
        if vertical == curr_player:
            return current-opponent
        # if evaluating the utility of the other player's potential moves
        return opponent - current

    def max_value(self, alpha, beta, limit, leaf_nodes, vertical, curr_player):
        if self.game_over(vertical) or limit == 0:
            return self.utility(vertical, curr_player), None, leaf_nodes+1
        v = float('-inf')
        best_move = None
        for a, a_board in self.successors(vertical):
            v2, a2, leaf_nodes = a_board.min_value(
                alpha, beta, limit-1, leaf_nodes, not vertical, curr_player)
            # print(f"move {a} has utility {v2}")
            if v2 > v:
                v, best_move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, best_move, leaf_nodes
        return v, best_move, leaf_nodes

    def min_value(self, alpha, beta, limit, leaf_nodes, vertical, curr_player):
        if self.game_over(vertical) or limit == 0:
            return self.utility(vertical, curr_player), None, leaf_nodes+1
        v = float('inf')
        best_move = None
        for a, a_board in self.successors(vertical):
            v2, a2, leaf_nodes = a_board.max_value(
                alpha, beta, limit-1, leaf_nodes, not vertical, curr_player)
            if v2 < v:
                v, best_move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, best_move, leaf_nodes
        return v, best_move, leaf_nodes

    # Required
    def get_best_move(self, vertical, limit):
        leaf_nodes = 0
        v, best_move, leaf_nodes = self.max_value(
            float('-inf'), float('inf'), limit, leaf_nodes, vertical, vertical)
        return (best_move, v, leaf_nodes)

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
15
"""

feedback_question_2 = """
Translating the alpha-beta search pseudocode from the textbook
into actual code that works for this particular game was the
most difficult part. More specifically, keeping track of all
the different booleans and variables to make sure that the utility
was being calculated correctly. It was confusing to trace the
recursive nature of this search algorithm for when I had bugs.
My biggest problem was making the utility function account
for if we are calculating for the current player, or we are
calculating potential utility for moves in the future for the
other player.
"""

feedback_question_3 = """
I like how this project got to reflect how real games work
when you have an opponent! The outline of the algorithm from the
textbook was super helpful. Wouldn't change anything.
"""
