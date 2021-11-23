# Reader for files from www.conwaylife.com/wiki

from io import TextIOBase
from typing import Set, Tuple


def read_cells_from_stream(stream: TextIOBase) -> Set[Tuple[int, int]]:
    nxt_line = stream.readline()

    y_curr = 0
    cells: Set[Tuple[int, int]] = set()
    while nxt_line:
        # Check for comment
        if nxt_line[0] != "!":
            for x_curr in range(len(nxt_line)):
                # Scan, checking for cells
                if nxt_line[x_curr] == "O":
                    cells.add((x_curr, y_curr))
            y_curr = y_curr + 1
        nxt_line = stream.readline()

    return cells
