import pytest
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
    lines = captured.out.strip().split('\n')
    assert lines[0] == 'x7xxxxxxx'
    for i in range(1, 9):
        assert lines[i] == 'x' * 9