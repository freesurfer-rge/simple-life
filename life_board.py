# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3

from typing import List, Tuple, Union

import numpy as np


class SparseSetState:
    def __init__(self, grid):
        self.grid = grid

    def copy(self):
        return SparseSetState(copy(self.grid))

    def get_neighbours(self, elem, x_max, y_max):
        # Returns the neighbours of a live cell if they lie
        # within the bounds of the grid specified
        l = []
        if elem[0] - 1 >= 0:
            l.append((elem[0] - 1, elem[1]))

        if elem[0] - 1 >= 0 and elem[1] - 1 >= 0:
            l.append((elem[0] - 1, elem[1] - 1))

        if elem[0] - 1 >= 0 and elem[1] + 1 < y_max:
            l.append((elem[0] - 1, elem[1] + 1))

        if elem[1] - 1 >= 0:
            l.append((elem[0], elem[1] - 1))

        if elem[1] - 1 >= 0 and elem[0] + 1 < x_max:
            l.append((elem[0] + 1, elem[1] - 1))

        if elem[1] + 1 < y_max:
            l.append((elem[0], elem[1] + 1))

        if elem[0] + 1 < x_max:
            l.append((elem[0] + 1, elem[1]))

        if elem[1] + 1 < y_max and elem[0] + 1 < x_max:
            l.append((elem[0] + 1, elem[1] + 1))

        return l

    def equals(self, other):
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(self, rules, x_size, y_size):
        # Calls the actual rules and provides them with the grid
        # and the neighbour function
        self.grid = rules.apply_rules(self.grid, x_size, y_size, self.get_neighbours)
        return self


class SparseSetRules:
    def apply_rules(self, grid, x_max, y_max, get_neighbours):
        # grid = state.grid
        counter = {}

        # Find all neighbours to active cells
        # and their counts of active cells
        for elem in grid:
            if elem not in counter:
                counter[elem] = 0

            nb = get_neighbours(elem, x_max, y_max)

            for n in nb:
                if n not in counter:
                    counter[n] = 1
                else:
                    counter[n] += 1

        # Apply rules of Life
        for c in counter:
            if counter[c] < 2 or counter[c] > 3:
                grid.discard(c)
            if counter[c] == 3:
                grid.add(c)

        return grid


class LifeBoard:
    def __init__(self, initial_state, rules, x_max, y_max):
        self.state = initial_state
        self.rules = rules
        self.x_max = x_max
        self.y_max = y_max

    def run_game(self):
        self.state = self.state.apply_rules(self.rules, self.x_max, self.y_max)
