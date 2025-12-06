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


def test_puzzle_print(capsys):
    puzzle = Puzzle()
    puzzle[0, 1] = Cell(value=7)
    puzzle.print()
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert lines[0] == "x7xxxxxxx"
    for i in range(1, 9):
        assert lines[i] == "x" * 9


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


def test_set_as_initial_state():
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle.set_as_initial_state()
    assert puzzle._initial_state is not None
    assert puzzle._initial_state[0][0].value == 1
    puzzle[0, 0] = Cell(value=2)
    assert puzzle._initial_state[0][0].value == 1
