import pytest

from typing import List, Set, Tuple

from sparse_set_state import SparseSetState


class TestGetNeighbours:
    def check_neighbours(
        self, actual: List[Tuple[int, int]], expected: Set[Tuple[int, int]]
    ):
        assert isinstance(actual, list)
        # Compare sets, since the neighbour order shouldn't matter
        assert set(actual) == expected

    @pytest.mark.parametrize(
        "cell,expected",
        [
            ((0, 0), {(0, 1), (1, 1), (1, 0)}),
            ((2, 2), {(1, 2), (1, 1), (2, 1)}),
            ((0, 2), {(1, 2), (1, 1), (0, 1)}),
            ((2, 0), {(2, 1), (1, 1), (1, 0)}),
        ],
        ids=["(0,0)", "(2,2)", "(0,2)", "(2,0)"],
    )
    def test_get_neighbours_corner(self, cell, expected):
        # Don't need any active cells
        target = SparseSetState({})

        actual = target.get_neighbours(cell, 2, 2)
        self.check_neighbours(actual, expected)
