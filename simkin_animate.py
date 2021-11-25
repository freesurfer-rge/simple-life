from typing import List, Tuple

from life import (
    LifeBoard,
    SparseSetRules,
    SparseSetState,
    read_cells_from_stream,
)


from PIL import Image, ImageDraw


nx = 1024
ny = 1024
dx = 500
dy = 500


def write_image(cells: List[Tuple[int, int]], name: str):
    image = Image.new("1", (nx, ny))
    for c in cells:
        image.putpixel((c[0], c[1]), 1)
    image.save(name)


def main():
    with open("life/pattern_files/simkinglidergun.cells", "r") as pf:
        pattern_from_file = read_cells_from_stream(pf)

    print("Read initial file")

    initial_pattern = [(c[0] + dx, c[1] + dy) for c in pattern_from_file]

    name_pattern = "image_{0:04}.png"
    iteration = 0

    write_image(initial_pattern, name_pattern.format(iteration))

    rules = SparseSetRules()
    state = SparseSetState(initial_pattern)
    board = LifeBoard(state, rules, nx, ny, x_wrap=True, y_wrap=True)

    for _ in range(500):
        board.update()
        iteration = iteration + 1
        write_image(board.state.grid, name_pattern.format(iteration))


main()
