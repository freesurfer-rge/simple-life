# Adapted from
# https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3

# Processes Life rules for a sparse board

from typing import Set, Func, Tuple

class SparseSetRules:
    def apply_rules(self, grid:Set(Tuple[int,int]), x_max: int, y_max:int, get_neighbours):
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