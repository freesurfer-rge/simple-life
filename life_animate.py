from sys import argv
from typing import Set, Tuple

from life import (
    LifeBoard,
    SparseSetRules,
    SparseSetState,
    read_cells_from_stream,
)


from PIL import Image, ImageDraw


nx = 256
ny = 256
dx = 120
dy = 120


def get_image(cells: Set[Tuple[int, int]]) -> Image:
    image = Image.new("L", (nx, ny))
    for c in cells:
        image.putpixel((c[0], c[1]), 255)
    return image


def write_image(cells: Set[Tuple[int, int]], name: str):
    image = get_image(cells)
    image.save(name)


def main(target_file):
    with open(target_file, "r") as pf:
        pattern_from_file = read_cells_from_stream(pf)

    print("Read initial file")

    initial_pattern = set([(c[0] + dx, c[1] + dy) for c in pattern_from_file])

    images = []
    images.append(get_image(initial_pattern))

    rules = SparseSetRules()
    state = SparseSetState(initial_pattern)
    board = LifeBoard(state, rules, nx, ny, x_wrap=True, y_wrap=True)

    for _ in range(10000):
        board.update()
        images.append(get_image(board.state.grid))

    images[0].save(
        "cells.gif", save_all=True, append_images=images[1:], duration=40
    )


main(argv[1])
