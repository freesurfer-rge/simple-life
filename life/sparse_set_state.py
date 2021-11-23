# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3

# Holds the state of a Life board as a set of active cells (Tuple(x,y))

from copy import copy
from typing import List, Set, Tuple
from typing_extensions import ParamSpec

from sparse_set_rules import SparseSetRules


class SparseSetState:
    def __init__(self, grid: Set[Tuple[int, int]]):
        self.grid = grid

    def copy(self) -> "SparseSetState":
        return SparseSetState(copy(self.grid))

    def get_neighbours(
        self, elem: Tuple[int, int], x_max: int, y_max: int
    ) -> List[Tuple[int, int]]:
        # Returns the neighbours of a live cell if they lie
        # within the bounds of the grid specified
        l: List[Tuple[int, int]] = []
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

    def equals(self, other: "SparseSetState") -> bool:
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(
        self, rules: "SparseSetRules", x_size: int, y_size: int
    ) -> "SparseSetState":
        # Calls the actual rules and provides them with the grid
        # and the neighbour function
        self.grid = rules.apply_rules(
            self.grid, x_size, y_size, self.get_neighbours
        )
        return self
