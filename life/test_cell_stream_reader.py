import pathlib

from .cell_stream_reader import read_cells_from_stream

current_file = pathlib.Path(__file__)
pattern_file_dir = current_file.parent / "pattern_files"


class TestCellStreamReader:
    def test_block(self):
        cells = set()
        with open(pattern_file_dir / "block.cells", "r") as fs:
            cells = read_cells_from_stream(fs)

        expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
        assert cells == expected

    def test_glider(self):
        cells = set()
        with open(pattern_file_dir / "glider.cells", "r") as fs:
            cells = read_cells_from_stream(fs)

        expected = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
        assert cells == expected
