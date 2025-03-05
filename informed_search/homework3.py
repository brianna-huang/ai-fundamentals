############################################################
# CIS 521: Homework 3
############################################################

import random
from queue import PriorityQueue
import math
student_name = "Brianna Huang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = []
    for row in range(rows):
        board.append([cols*row+1+i for i in range(cols)])
    board[rows-1][cols-1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.empty = []
        for ind, row in enumerate(self.board):
            if 0 in row:
                self.empty = [ind, row.index(0)]

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        row = self.empty[0]
        col = self.empty[1]
        if direction == 'up' and row-1 >= 0:
            # set the empty cell to the cell above it
            self.board[row][col] = self.board[row-1][col]
            # set the cell above to the empty one
            self.board[row-1][col] = 0
            self.empty = [row-1, col]
            return True
        if direction == 'down' and row+1 < self.rows:
            # set the empty cell to the cell below it
            self.board[row][col] = self.board[row+1][col]
            # set the cell below to the empty one
            self.board[row+1][col] = 0
            self.empty = [row+1, col]
            return True
        if direction == 'left' and col-1 >= 0:
            self.board[row][col] = self.board[row][col-1]
            self.board[row][col-1] = 0
            self.empty = [row, col-1]
            return True
        if direction == 'right' and col+1 < self.cols:
            self.board[row][col] = self.board[row][col+1]
            self.board[row][col+1] = 0
            self.empty = [row, col+1]
            return True
        return False

    def scramble(self, num_moves):
        for _ in range(num_moves):
            self.perform_move(random.choice(['up', 'down', 'left', 'right']))

    def is_solved(self):
        solved_board = []
        for row in range(self.rows):
            solved_board.append([self.cols*row+1+i for i in range(self.cols)])
        solved_board[self.rows-1][self.cols-1] = 0
        return self.board == solved_board

    def copy(self):
        return TilePuzzle([row[:] for row in self.board])

    def successors(self):
        for direction in ['up', 'down', 'right', 'left']:
            new_board = self.copy()
            if new_board.perform_move(direction):
                yield direction, new_board

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
        if limit == 0:
            return
        for direction, new_board in self.successors():
            visiting = moves + [direction]
            for solution in new_board.iddfs_helper(limit-1, visiting):
                yield solution

    # Required
    def find_solutions_iddfs(self):
        depth = 0
        solutions = []
        while len(solutions) <= 0:
            solutions = list(self.iddfs_helper(depth, []))
            if solutions:
                for solution in solutions:
                    yield solution
            depth += 1

    def manhattan(self):
        total_dist = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell > 0:
                    correct_row = (cell-1)//self.cols
                    correct_col = (cell-1) % self.cols
                    total_dist += abs(row-correct_row) + abs(col-correct_col)
        return total_dist

    # Required
    def find_solution_a_star(self):
        frontier = PriorityQueue()
        # (priority heuristic, current board, moves)
        frontier.put((self.manhattan(), self.board, []))

        board = tuple(tuple(row) for row in self.board)
        visited = set(board)

        while not frontier.empty():
            md, curr, moves = frontier.get()
            curr = TilePuzzle(curr)
            if curr.is_solved():
                return moves
            for direction, new_board in curr.successors():
                visiting = tuple(tuple(r) for r in new_board.board)
                if visiting not in visited:
                    visited.add(visiting)
                    priority = self.manhattan() + len(moves)
                    frontier.put(
                        (priority, new_board.board, moves+[direction]))
        return []


############################################################
# Section 2: Grid Navigation
############################################################

def euclidian(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)


def find_path(start, goal, scene):
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None

    frontier = PriorityQueue()
    # (heuristic, total cost so far, current location, moves)
    frontier.put((euclidian(start, goal), 0, start))

    came_from = {}
    came_from[start] = None
    costs = {start: 0}
    visited = set(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while not frontier.empty():
        estimate, cost, location = frontier.get()
        if location == goal:
            path = []
            while location != start:
                path.append(location)
                location = came_from[location]
            path.append(start)
            path.reverse()
            return path

        for x, y in directions:
            visiting = (location[0]+x, location[1]+y)
            # check if in bounds & not an obstacle
            if (0 <= visiting[0] < len(scene)
                    and 0 <= visiting[1] < len(scene[0])
                    and not scene[location[0]][location[1]]
                    and visiting not in visited):
                # total cost with visiting node
                new_cost = cost + euclidian(location, visiting)
                # total estimated cost
                priority = new_cost + euclidian(visiting, goal)

                if visiting not in costs or new_cost < costs[visiting]:
                    costs[visiting] = new_cost
                    frontier.put((priority, new_cost, visiting))
                    came_from[visiting] = location
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def manhattan(board, length, n):
    end = tuple(range(length-1, length - n - 1, -1))
    return sum(abs(board[i] - end[i]) for i in range(n))/2


def solve_distinct_disks(length, n):
    start = tuple(range(n))
    end = tuple(range(length-1, length - n - 1, -1))

    # (heuristic, total cost so far, current board, list of moves)
    frontier = PriorityQueue()
    frontier.put((manhattan(start, length, n), 0, start, []))
    visited = set([start])

    while not frontier.empty():
        estimate, cost, curr, moves = frontier.get()
        if curr == end:
            return moves
        # iterate through all possible moves for each disk
        for i in range(n):
            if curr[i] + 1 < length and curr[i] + 1 not in curr:
                visiting = list(curr)
                visiting[i] = visiting[i] + 1
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.put((manhattan(visiting, length, n)+(cost+1),
                                  cost+1, visiting,
                                  moves+[(curr[i], curr[i]+1)]))
                    visited.add(visiting)
            if (curr[i] + 2 < length and curr[i] + 2 not in curr
                    and curr[i] + 1 in curr):
                visiting = list(curr)
                visiting[i] = visiting[i] + 2
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.put((manhattan(visiting, length, n)+(cost+1),
                                  cost+1, visiting,
                                  moves + [(curr[i], curr[i]+2)]))
                    visited.add(visiting)
            if curr[i] - 1 >= 0 and curr[i] - 1 not in curr:
                visiting = list(curr)
                visiting[i] = visiting[i] - 1
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.put((manhattan(visiting, length, n)+(cost+1),
                                  cost+1, visiting,
                                  moves + [(curr[i], curr[i]-1)]))
                    visited.add(visiting)
            if (curr[i] - 2 >= 0 and curr[i] - 2 not in curr
                    and curr[i] - 1 in curr):
                visiting = list(curr)
                visiting[i] = visiting[i] - 2
                visiting = tuple(visiting)
                if visiting not in visited:
                    frontier.put((manhattan(visiting, length, n)+(cost+1),
                                  cost+1, visiting,
                                  moves + [(curr[i], curr[i]-2)]))
                    visited.add(visiting)
    return []

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
12
"""

feedback_question_2 = """
The assignment overall was just pretty challenging. I very
slowly got used to the basic layout of an A* search algorithm,
but I was pretty stuck on the IDDFS parts, since I'm new to
using generators.
"""

feedback_question_3 = """
Per usual, I liked being able to test out my implementation
on the GUI. It's fun to be able to see my algorithm reflect
directly on how it performs on the game. Wouldn't change
anything about the assignment, seems reasonable.
"""
