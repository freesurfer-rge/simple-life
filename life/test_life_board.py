from .life_board import LifeBoard
from .sparse_set_rules import SparseSetRules
from .sparse_set_state import SparseSetState


class TestLifeBoard:
    def test_single_cell_dies(self):
        nx = 4
        ny = 4

        initial_state = {(1, 1)}

        rules = SparseSetRules()
        state = SparseSetState(initial_state)

        board = LifeBoard(state, rules, nx, ny)

        # Check construction
        assert board.state.grid == initial_state

        # Update
        board.update()

        # Cell should be dead
        assert board.state.grid == set()

    def test_square_stable(self):
        nx = 4
        ny = 4

        initial_state = {(1, 1), (1, 2), (2, 1), (2, 2)}

        rules = SparseSetRules()
        state = SparseSetState(initial_state)
        board = LifeBoard(state, rules, nx, ny)

        # Check construction
        assert board.state.grid == initial_state

        # Update
        board.update()

        # Should be unchanged
        assert board.state.grid == initial_state

    def test_square_stable_exact(self):
        nx = 2
        ny = 2

        initial_state = {(0, 0), (0, 1), (1, 0), (1, 1)}
        rules = SparseSetRules()
        state = SparseSetState(initial_state)
        board = LifeBoard(state, rules, nx, ny)

        # Check construction
        assert board.state.grid == initial_state

        # Update
        board.update()

        # Should be unchanged
        assert board.state.grid == initial_state

    def test_rotor_rotates(self):
        nx = 3
        ny = 3

        initial_state = {(0, 1), (1, 1), (2, 1)}

        rules = SparseSetRules()
        state = SparseSetState(initial_state)
        board = LifeBoard(state, rules, nx, ny)

        # Check construction
        assert board.state.grid == initial_state

        # Update
        board.update()
        assert board.state.grid == {(1, 0), (1, 1), (1, 2)}

        # And update again
        board.update()
        assert board.state.grid == initial_state
