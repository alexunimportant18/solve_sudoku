import pytest
from sudoku.cell import Cell

def test_cell_initialization():
    cell = Cell()
    assert cell.value is None
    assert cell.possible_values == {1, 2, 3, 4, 5, 6, 7, 8, 9}

def test_cell_initialization_with_value():
    cell = Cell(value=5)
    assert cell.value == 5
    assert cell.possible_values == {1, 2, 3, 4, 5, 6, 7, 8, 9}

def test_set_value():
    cell = Cell()
    cell.set_value(7)
    assert cell.value == 7
    assert cell.possible_values == {7}

def test_set_value_with_possible():
    cell = Cell()
    cell.set_value(7, {7, 8})
    assert cell.value == 7
    assert cell.possible_values == {7, 8}

def test_cell_equality():
    cell1 = Cell(value=5)
    cell2 = Cell(value=5)
    cell3 = Cell(value=6)
    cell4 = Cell(value=5, possible_values={5})

    assert cell1 == cell2
    assert cell1 != cell3
    assert cell1 != cell4

    cell1.set_value(5)
    assert cell1 == cell4