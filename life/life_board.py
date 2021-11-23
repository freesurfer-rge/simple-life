# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3


from .sparse_set_rules import SparseSetRules
from .sparse_set_state import SparseSetState


class LifeBoard:
    def __init__(
        self,
        initial_state: SparseSetState,
        rules: SparseSetRules,
        x_max: int,
        y_max: int,
        x_wrap: bool = False,
        y_wrap: bool = False,
    ):
        self.state = initial_state
        self.rules = rules
        self.x_max = x_max
        self.y_max = y_max
        self.x_wrap = x_wrap
        self.y_wrap = y_wrap

    def update(self):
        self.state = self.state.apply_rules(
            self.rules, self.x_max, self.y_max, self.x_wrap, self.y_wrap
        )
