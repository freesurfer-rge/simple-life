# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3

# Processes Life rules for a board store as a spare set of active cells

from typing import Callable, Dict, List, Set, Tuple


class SparseSetRules:
    def apply_rules(
        self,
        grid: Set[Tuple[int, int]],
        x_max: int,
        y_max: int,
        get_neighbours: Callable[
            [Tuple[int, int], int, int], List[Tuple[int, int]]
        ],
    ) -> Set[Tuple[int, int]]:
        # grid = state.grid
        counter: Dict[Tuple[int, int], int] = {}

        # Find all neighbours to active cells
        # and their counts of active cells
        for elem in grid:
            if elem not in counter:
                counter[elem] = 0

            nb: List[Tuple[int, int]] = get_neighbours(elem, x_max, y_max)

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
