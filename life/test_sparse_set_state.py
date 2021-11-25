import pytest

from typing import List, Set, Tuple

from .sparse_set_state import SparseSetState


class TestGetNeighboursNoWrap:
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

        actual = target.get_neighbours(cell, 3, 3)
        self.check_neighbours(actual, expected)

    @pytest.mark.parametrize(
        "cell, expected",
        [
            ((1, 0), {(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)}),
            ((0, 1), {(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)}),
            ((1, 2), {(0, 2), (0, 1), (1, 1), (2, 1), (2, 2)}),
            ((2, 1), {(2, 0), (1, 0), (1, 1), (1, 2), (2, 2)}),
        ],
        ids=["(1,0)", "(0,1)", "(1,2)", "(2,1)"],
    )
    def test_get_neighbours_edge(self, cell, expected):
        # Don't need any active cells
        target = SparseSetState({})

        actual = target.get_neighbours(cell, 3, 3)
        self.check_neighbours(actual, expected)

    def test_get_neighbours_centre(self):
        # Don't need any active cells
        target = SparseSetState({})

        actual = target.get_neighbours((1, 1), 3, 3)
        expected = {
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        }
        self.check_neighbours(actual, expected)


class TestGetNeighboursWrap3x3:
    def check_neighbours(
        self, actual: List[Tuple[int, int]], expected: Set[Tuple[int, int]]
    ):
        assert isinstance(actual, list)
        # Compare sets, since the neighbour order shouldn't matter
        assert set(actual) == expected

    @pytest.mark.parametrize(
        "cell",
        [(0, 0), (2, 2), (0, 2), (2, 0)],
        ids=["(0,0)", "(2,2)", "(0,2)", "(2,0)"],
    )
    def test_get_neighbours_corner(self, cell):
        nx = 3
        ny = 3
        # Don't need any active cells
        target = SparseSetState({})

        # With wrapping everything should neighbour everything on a 3x3
        expected: Set[Tuple[int, int]] = set()
        for i in range(nx):
            for j in range(ny):
                expected.add((i, j))
        expected.discard(cell)

        actual = target.get_neighbours(cell, nx, ny, x_wrap=True, y_wrap=True)
        self.check_neighbours(actual, expected)

    @pytest.mark.parametrize(
        "cell",
        [(0, 1), (1, 0), (2, 1), (1, 2)],
        ids=["(0,1)", "(1,0)", "(2,1)", "(1,2)"],
    )
    def test_get_neighbours_edge(self, cell):
        nx = 3
        ny = 3
        # Don't need any active cells
        target = SparseSetState({})

        # With wrapping everything should neighbour everything on a 3x3
        expected: Set[Tuple[int, int]] = set()
        for i in range(nx):
            for j in range(ny):
                expected.add((i, j))
        expected.discard(cell)

        actual = target.get_neighbours(cell, nx, ny, x_wrap=True, y_wrap=True)
        self.check_neighbours(actual, expected)

    def test_get_neighbours_centre(self):
        # Don't need any active cells
        target = SparseSetState({})

        actual = target.get_neighbours((1, 1), 3, 3, x_wrap=True, y_wrap=True)
        expected = {
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        }
        self.check_neighbours(actual, expected)


class TestGetNeighboursWrap5x5:
    def fetch_neighbours(self, target_cell: Tuple[int, int]):
        target = SparseSetState({})

        neighbours = target.get_neighbours(
            target_cell, 5, 5, x_wrap=True, y_wrap=True
        )
        return neighbours

    def check_neighbours(
        self, actual: List[Tuple[int, int]], expected: Set[Tuple[int, int]]
    ):
        assert isinstance(actual, list)
        assert len(expected) == 8  # With wrapping, always have 8 neighbours
        assert len(actual) == 8
        # Compare sets, since the neighbour order shouldn't matter
        assert set(actual) == expected

    def test_check_centre(self):
        actual = self.fetch_neighbours(target_cell=(2, 2))
        expected = {
            (1, 1),
            (2, 1),
            (3, 1),
            (1, 2),
            (3, 2),
            (1, 3),
            (2, 3),
            (3, 3),
        }
        self.check_neighbours(actual, expected)

    @pytest.mark.parametrize(
        "cell,expected",
        [
            (
                (2, 1),
                {
                    (1, 0),
                    (2, 0),
                    (3, 0),
                    (1, 1),
                    (3, 1),
                    (1, 2),
                    (2, 2),
                    (3, 2),
                },
            ),
            (
                (1, 2),
                {
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (1, 1),
                    (1, 3),
                    (2, 1),
                    (2, 2),
                    (2, 3),
                },
            ),
            (
                (2, 3),
                {
                    (1, 2),
                    (2, 2),
                    (3, 2),
                    (1, 3),
                    (3, 3),
                    (1, 4),
                    (2, 4),
                    (3, 4),
                },
            ),
            (
                (3, 2),
                {
                    (2, 1),
                    (2, 2),
                    (2, 3),
                    (3, 1),
                    (3, 3),
                    (4, 1),
                    (4, 2),
                    (4, 3),
                },
            ),
        ],
        ids=["(2,1)", "(1,2)", "(2,3)", "(3,2)"],
    )
    def test_touch_edge(self, cell, expected):
        actual = self.fetch_neighbours(cell)
        self.check_neighbours(actual, expected)

    @pytest.mark.parametrize(
        "cell,expected",
        [
            (
                (2, 0),
                {
                    (1, 4),
                    (2, 4),
                    (3, 4),
                    (1, 0),
                    (3, 0),
                    (1, 1),
                    (2, 1),
                    (3, 1),
                },
            ),
            (
                (0, 2),
                {
                    (4, 1),
                    (4, 2),
                    (4, 3),
                    (0, 1),
                    (0, 3),
                    (1, 1),
                    (1, 2),
                    (1, 3),
                },
            ),
            (
                (2, 4),
                {
                    (1, 3),
                    (2, 3),
                    (3, 3),
                    (1, 4),
                    (3, 4),
                    (1, 0),
                    (2, 0),
                    (3, 0),
                },
            ),
            (
                (4, 2),
                {
                    (3, 1),
                    (3, 2),
                    (3, 3),
                    (4, 1),
                    (4, 3),
                    (0, 1),
                    (0, 2),
                    (0, 3),
                },
            ),
        ],
        ids=["(2,0)", "(0,2)", "(2,4)", "(4,2)"],
    )
    def test_overlap_edge(self, cell, expected):
        actual = self.fetch_neighbours(cell)
        self.check_neighbours(actual, expected)
