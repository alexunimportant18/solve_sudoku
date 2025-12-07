from sudoku.puzzle import Puzzle
from sudoku.cell import Cell


def test_puzzle_initialization():
    puzzle = Puzzle()
    assert isinstance(puzzle, Puzzle)
    for i in range(9):
        for j in range(9):
            assert isinstance(puzzle[i, j], Cell)
            assert puzzle[i, j].value is None
            assert puzzle[i, j].possible_values == set(range(1, 10))


def test_puzzle_getitem_setitem():
    puzzle = Puzzle()
    cell = Cell(value=5)
    puzzle[0, 0] = cell
    assert puzzle[0, 0] is cell
    assert puzzle[0, 0].value == 5

    cell2 = Cell(value=9)
    puzzle[8, 8] = cell2
    assert puzzle[8, 8] is cell2
    assert puzzle[8, 8].value == 9

def test_puzzle_eq():
    puzzle1 = Puzzle()
    puzzle2 = Puzzle()
    assert puzzle1 == puzzle2

    puzzle1[0, 0] = Cell(value=1)
    assert puzzle1 != puzzle2

    puzzle2[0, 0] = Cell(value=1)
    assert puzzle1 == puzzle2

    puzzle2[0, 0] = Cell(value=2)
    assert puzzle1 != puzzle2


def test_print_unsolved_values(capsys):
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle[0, 1].possible_values = {2, 3}
    puzzle.print_unsolved_values()
    captured = capsys.readouterr()
    assert "Cell (0, 1) has possible values {2, 3}" in captured.out
    assert "Cell (0, 0)" not in captured.out


def test_update_single_possible_values():
    puzzle = Puzzle()
    puzzle[0, 0].possible_values = {5}
    puzzle.update_single_possible_values()
    assert puzzle[0, 0].value == 5


def test_get_unsolved_cells():
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    unsolved = puzzle.get_unsolved_cells()
    assert len(unsolved) == 80
    for tile in unsolved:
        assert tile.position != (0, 0)

def test_is_solved():
    puzzle = Puzzle()
    assert not puzzle.is_solved()
    for i in range(9):
        for j in range(9):
            # This is not a valid sudoku, but it is "solved" in the sense that every cell has a value
            puzzle[i, j] = Cell(value=(i + j) % 9 + 1)
    assert puzzle.is_solved()

def test_is_valid_group():
    from sudoku.tile import Tile
    puzzle = Puzzle()
    tiles = [
        Tile(position=(0, 0), cell=Cell(value=1)),
        Tile(position=(0, 1), cell=Cell(value=2)),
        Tile(position=(0, 2), cell=Cell(value=3)),
    ]
    assert puzzle._is_valid_group(tiles)

    tiles_with_duplicate = [
        Tile(position=(0, 0), cell=Cell(value=1)),
        Tile(position=(0, 1), cell=Cell(value=1)),
    ]
    assert not puzzle._is_valid_group(tiles_with_duplicate)

    tiles_with_none = [
        Tile(position=(0, 0), cell=Cell(value=1)),
        Tile(position=(0, 1), cell=Cell(value=None)),
    ]
    assert puzzle._is_valid_group(tiles_with_none)


def test_is_valid():
    puzzle = Puzzle()
    assert puzzle.is_valid()

    # row violation
    puzzle[0, 0] = Cell(value=1)
    puzzle[0, 1] = Cell(value=1)
    assert not puzzle.is_valid()

    # col violation
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle[1, 0] = Cell(value=1)
    assert not puzzle.is_valid()

    # section violation
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle[1, 1] = Cell(value=1)
    assert not puzzle.is_valid()

    # valid puzzle
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle[0, 1] = Cell(value=2)
    puzzle[1, 0] = Cell(value=3)
    puzzle[1, 1] = Cell(value=4)
    assert puzzle.is_valid()