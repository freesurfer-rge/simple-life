import numpy as np

from boundary_conditions import BoundaryConditions
from life_board import LifeBoard


class TestBasic:
    def test_constructor(self):
        lb = LifeBoard(
            32, 64, BoundaryConditions.EMPTY, BoundaryConditions.WRAP
        )

        assert isinstance(lb.board, np.ndarray)
        assert lb.board.shape == (64, 32)  # C style ordering
        assert np.all(lb.board == 0)
        assert lb.x_boundary == BoundaryConditions.EMPTY
        assert lb.y_boundary == BoundaryConditions.WRAP

    def test_simple_set(self):
        nx = 2
        ny = 3
        lb = LifeBoard(
            nx, ny, BoundaryConditions.EMPTY, BoundaryConditions.EMPTY
        )
        assert np.all(lb.board == 0)

        lb.set_cells([(0, 1)])
        for i in range(ny):
            for j in range(nx):
                if i == 1 and j == 0:
                    assert lb.board[i, j] == 1
                else:
                    assert lb.board[i, j] == 0

    def test_set_two(self):
        nx = 2
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.EMPTY, BoundaryConditions.EMPTY
        )
        assert np.all(lb.board == 0)

        lb.set_cells([(0, 1), (0, 0)])
        assert lb.board[0, 0] == 1
        assert lb.board[1, 0] == 1
        assert lb.board.sum() == 2

    def test_set_three(self):
        nx = 3
        ny = 4

        lb = LifeBoard(
            nx, ny, BoundaryConditions.EMPTY, BoundaryConditions.EMPTY
        )
        assert np.all(lb.board == 0)
        lb.set_cells([[0, 1], [1, 2], [0, 3]])
        assert lb.board[1, 0] == 1
        assert lb.board[2, 1] == 1
        assert lb.board[3, 0] == 1
        assert lb.board.sum() == 3


class TestShiftForNeighboursWrap:
    def test_x_only(self):
        nx = 3
        ny = 2

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 1), (1, 1)])

        # Looking at increasing x
        shifted = lb.shift_for_neighbours(1, 0)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 2
        assert shifted[1, 1] == 1
        assert shifted[1, 2] == 1

        # Looking at decreasing x
        shifted = lb.shift_for_neighbours(-1, 0)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 2
        assert shifted[1, 0] == 1
        assert shifted[1, 2] == 1

    def test_y_only(self):
        nx = 2
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 1), (0, 2)])

        # Look at decreasing y, should have two cells with neighbours
        shifted = lb.shift_for_neighbours(0, -1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 2
        assert shifted[0, 0] == 1
        assert shifted[1, 0] == 1

        # Look at increasing y, should still have two
        shifted = lb.shift_for_neighbours(0, 1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 2
        assert shifted[2, 0] == 1
        assert shifted[0, 0] == 1

    def test_both(self):
        nx = 3
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 0), (0, 1), (1, 0), (1, 1)])

        # Both positive
        shifted = lb.shift_for_neighbours(1, 1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 4
        assert shifted[1, 1] == 1
        assert shifted[1, 2] == 1
        assert shifted[2, 1] == 1
        assert shifted[2, 2] == 1

        # Both negative
        shifted = lb.shift_for_neighbours(-1, -1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 4
        assert shifted[0, 0] == 1
        assert shifted[0, 2] == 1
        assert shifted[2, 0] == 1
        assert shifted[2, 2] == 1

        # x positive, y negative
        shifted = lb.shift_for_neighbours(1, -1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 4
        assert shifted[0, 1] == 1
        assert shifted[0, 2] == 1
        assert shifted[2, 1] == 1
        assert shifted[2, 2] == 1

        # x negative, y positive
        shifted = lb.shift_for_neighbours(-1, 1)
        assert np.all(np.logical_or((shifted == 1), (shifted == 0)))
        assert shifted.sum() == 4
        assert shifted[1, 0] == 1
        assert shifted[1, 2] == 1
        assert shifted[2, 0] == 1
        assert shifted[2, 2] == 1


class TestGetNeighbourCountsWrap:
    def test_wrapping_01(self):
        nx = 5
        ny = 5

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(2, 2)])

        counts = lb.get_neighbour_counts()
        assert counts.sum() == 8
        assert counts[1, 1] == 1
        assert counts[1, 2] == 1
        assert counts[1, 3] == 1
        assert counts[2, 1] == 1
        assert counts[2, 3] == 1
        assert counts[3, 1] == 1
        assert counts[3, 2] == 1
        assert counts[3, 3] == 1

    def test_wrapping_02(self):
        nx = 3
        ny = 2

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 1), (1, 1)])

        counts = lb.get_neighbour_counts()
        assert counts[0, 0] == 4
        assert counts[0, 1] == 4
        assert counts[0, 2] == 4
        assert counts[1, 0] == 1
        assert counts[1, 1] == 1
        assert counts[1, 2] == 2

    def test_wrapping_03(self):
        nx = 3
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 1), (1, 1)])

        counts = lb.get_neighbour_counts()
        assert counts[0, 0] == 2
        assert counts[0, 1] == 2
        assert counts[0, 2] == 2
        assert counts[1, 0] == 1
        assert counts[1, 1] == 1
        assert counts[1, 2] == 2
        assert counts[2, 0] == 2
        assert counts[2, 1] == 2
        assert counts[2, 2] == 2


class TestGetNextBoardWrap:
    def test_single_cell_dies(self):
        nx = 3
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 0)])

        next = lb.get_next_board()
        assert next.sum() == 0

    def test_2x2square_survives(self):
        nx = 3
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 0), (1, 0), (0, 1), (1, 1)])

        nxt = lb.get_next_board()

        assert np.array_equal(nxt, lb.board)

    def test_simple_rotor(self):
        nx = 5
        ny = 5

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        # Rotor points left-right
        lb.set_cells([(1, 2), (2, 2), (3, 2)])

        nxt = lb.get_next_board()

        # Should now point up/down (but remember the ndarrays have coords [y,x])
        assert nxt.sum() == 3
        assert nxt[1, 2] == 1
        assert nxt[2, 2] == 1
        assert nxt[3, 2] == 1


class TestUpdate:
    def test_2x2square(self):
        nx = 3
        ny = 3

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        lb.set_cells([(0, 0), (1, 0), (0, 1), (1, 1)])

        lb.update()
        lb.update()

        expected = np.asarray([[1, 1, 0], [1, 1, 0], [0, 0, 0]], dtype=np.int8)
        assert np.array_equal(expected, lb.board)

    def test_rotor(self):
        nx = 5
        ny = 5

        lb = LifeBoard(
            nx, ny, BoundaryConditions.WRAP, BoundaryConditions.WRAP
        )
        # Rotor points left-right
        lb.set_cells([(1, 2), (2, 2), (3, 2)])

        lb.update()
        expected = np.asarray(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            dtype=np.int8,
        )
        assert np.array_equal(expected, lb.board)

        lb.update()
        expected = np.asarray(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            dtype=np.int8,
        )
        assert np.array_equal(expected, lb.board)
