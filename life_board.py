from typing import List, Tuple, Union

import numpy as np

from boundary_conditions import BoundaryConditions


def compute_new_state(current_state: np.int8, neighbour_count: np.int8):
    new_state = 0

    if neighbour_count == 3:
        new_state = 1  # Born or survives with three neighbours
    elif current_state == 1 and neighbour_count == 2:
        new_state = 1  # Also survives with two neighbours

    return new_state


array_compute_new_state = np.frompyfunc(compute_new_state, 2, 1)


class LifeBoard:
    def __init__(
        self,
        n_cells_x: int,
        n_cells_y: int,
        x_boundary: BoundaryConditions,
        y_boundary: BoundaryConditions,
    ):
        assert n_cells_x > 0, "Checking n_cells_x"
        assert n_cells_y > 0, "Checking n_cells_y"

        self._board = np.zeros((n_cells_y, n_cells_x), dtype=np.int8, order="C")
        self._x_boundary = x_boundary
        self._y_boundary = y_boundary

    @property
    def board(self) -> np.ndarray:
        return self._board

    @property
    def x_boundary(self) -> BoundaryConditions:
        return self._x_boundary

    @property
    def y_boundary(self) -> BoundaryConditions:
        return self._y_boundary

    def set_cells(self, cell_list: List[Union[Tuple[int, int], List[int]]]):
        for c in cell_list:
            assert len(c) == 2, "Checking length"
            assert c[0] >= 0, "Check x>=0"
            assert c[0] < self._board.shape[1], "Check x<nx"
            assert c[1] >= 0, "Check y>=0"
            assert c[1] < self._board.shape[0], "Check y<ny"
            self._board[c[1], c[0]] = 1

    def shift_for_neighbours(self, x_shift: int, y_shift: int):
        assert abs(x_shift) <= 1, "Check x_shift"
        assert abs(y_shift) <= 1, "Check y_shift"
        assert not (x_shift == 0 and y_shift == 0), "Don't self-neighbour"
        assert (
            self.x_boundary == BoundaryConditions.WRAP
        ), "Non-wrapping boundaries not supported yet"
        assert (
            self.y_boundary == BoundaryConditions.WRAP
        ), "Non-wrapping boundaries not supported yet"

        shifted_x = np.roll(self.board, shift=x_shift, axis=1)
        shifted_y = np.roll(shifted_x, shift=y_shift, axis=0)

        return shifted_y

    def get_neighbour_counts(self):
        shifts = [-1, 0, 1]
        counts = np.zeros_like(self.board)
        for i in shifts:
            for j in shifts:
                if i != 0 or j != 0:
                    neighbours = self.shift_for_neighbours(j, i)
                    counts = counts + neighbours
        return counts

    def get_next_board(self):
        neighbours = self.get_neighbour_counts()

        result = array_compute_new_state(self.board, neighbours)

        return result
