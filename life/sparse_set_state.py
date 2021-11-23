# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3

# Holds the state of a Life board as a set of active cells (Tuple(x,y))

from copy import copy
from typing import List, Set, Tuple

import numpy as np

from .sparse_set_rules import SparseSetRules


class SparseSetState:
    def __init__(self, grid: Set[Tuple[int, int]]):
        self.grid = grid

    def copy(self) -> "SparseSetState":
        return SparseSetState(copy(self.grid))

    def get_neighbours(
        self,
        elem: Tuple[int, int],
        x_size: int,
        y_size: int,
        x_wrap: bool = False,
        y_wrap: bool = False,
    ) -> List[Tuple[int, int]]:
        # Returns the neighbours of a live cell if they lie
        # within the bounds of the grid specified
        l: List[Tuple[int, int]] = []

        steps = [-1, 0, 1]
        for dx in steps:
            x_neighbour_pos = elem[0] + dx
            if x_wrap:
                x_neighbour_pos = x_neighbour_pos % x_size
            for dy in steps:
                if dx == 0 and dy == 0:
                    continue
                y_neighbour_pos = elem[1] + dy
                if y_wrap:
                    y_neighbour_pos = y_neighbour_pos % y_size

                if (
                    x_neighbour_pos >= 0
                    and x_neighbour_pos < x_size
                    and y_neighbour_pos >= 0
                    and y_neighbour_pos < y_size
                ):
                    l.append((x_neighbour_pos, y_neighbour_pos))

        return l

    def equals(self, other: "SparseSetState") -> bool:
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(
        self,
        rules: "SparseSetRules",
        x_size: int,
        y_size: int,
        x_wrap: bool = False,
        y_wrap: bool = False,
    ) -> "SparseSetState":
        # Calls the actual rules and provides them with the grid
        # and the neighbour function
        self.grid = rules.apply_rules(
            self.grid, x_size, y_size, self.get_neighbours, x_wrap, y_wrap
        )
        return self

    def to_dense(self, x_size: int, y_size: int) -> np.ndarray:
        result = np.zeros((y_size, x_size), dtype=np.uint8)

        for c in self.grid:
            result[c[1], c[0]] = 1

        return result
