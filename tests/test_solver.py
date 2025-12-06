import pytest
from sudoku.puzzle import Puzzle
from sudoku.cell import Cell
from sudoku.solver import (
    generate_sections,
    generate_rows,
    generate_cols,
    extract_cyclic_tiles,
    reduce_possible_tiles,
    step,
    Tile,
)


@pytest.fixture
def empty_puzzle():
    return Puzzle()


@pytest.fixture
def simple_puzzle():
    puzzle = Puzzle()
    puzzle[0, 0] = Cell(value=1)
    puzzle[0, 1] = Cell(value=2)
    puzzle[1, 0] = Cell(value=3)
    return puzzle


def test_generate_sections(empty_puzzle):
    sections = list(generate_sections(empty_puzzle))
    assert len(sections) == 9
    for section in sections:
        assert len(section) == 9
        positions = {tile.position for tile in section}
        assert len(positions) == 9


def test_generate_rows(empty_puzzle):
    rows = list(generate_rows(empty_puzzle))
    assert len(rows) == 9
    for i, row in enumerate(rows):
        assert len(row) == 9
        for j, tile in enumerate(row):
            assert tile.position == (i, j)


def test_generate_cols(empty_puzzle):
    cols = list(generate_cols(empty_puzzle))
    assert len(cols) == 9
    for i, col in enumerate(cols):
        assert len(col) == 9
        for j, tile in enumerate(col):
            assert tile.position == (j, i)


def test_extract_cyclic_tiles_no_cyclic():
    tiles = [
        Tile((0, 0), Cell(possible_values={1, 2})),
        Tile((0, 1), Cell(possible_values={1, 2, 3})),
        Tile((0, 2), Cell(value=4)),
    ]
    known, cyclic, remaining = extract_cyclic_tiles(tiles)
    assert len(known) == 1
    assert known[0].cell.value == 4
    assert len(cyclic) == 0
    assert len(remaining) == 2


def test_extract_cyclic_tiles_pair_and_known():
    tiles = [
        Tile((0, 0), Cell(possible_values={1, 2})),
        Tile((0, 1), Cell(possible_values={1, 2})),
        Tile((0, 2), Cell(possible_values={1, 2, 3})),
    ]
    known, cyclic, remaining = extract_cyclic_tiles(tiles)
    assert len(known) == 1
    assert known[0].position == (0, 2)
    assert known[0].cell.value == 3
    assert len(cyclic) == 2
    assert Tile((0, 0), Cell(possible_values={1, 2})) in cyclic
    assert Tile((0, 1), Cell(possible_values={1, 2})) in cyclic
    assert len(remaining) == 0


def test_extract_cyclic_tiles_pair_and_reduced():
    tiles = [
        Tile((0, 0), Cell(possible_values={1, 2})),
        Tile((0, 1), Cell(possible_values={1, 2})),
        Tile((0, 2), Cell(possible_values={1, 2, 3, 4})),
    ]
    known, cyclic, remaining = extract_cyclic_tiles(tiles)
    assert len(known) == 0
    assert len(cyclic) == 2
    assert Tile((0, 0), Cell(possible_values={1, 2})) in cyclic
    assert Tile((0, 1), Cell(possible_values={1, 2})) in cyclic
    assert len(remaining) == 1
    assert remaining[0].position == (0, 2)
    assert remaining[0].cell.possible_values == {3, 4}


def test_extract_cyclic_tiles_reduces_to_known():
    tiles = [
        Tile((0, 0), Cell(value=1)),
        Tile((0, 1), Cell(possible_values={1, 2})),
        Tile((0, 2), Cell(possible_values={3, 4})),
    ]
    known, cyclic, remaining = extract_cyclic_tiles(tiles)
    assert len(known) == 2
    assert len(cyclic) == 0
    assert len(remaining) == 1
    known_positions = {tile.position for tile in known}
    assert (0, 0) in known_positions
    assert (0, 1) in known_positions
    known_values = {tile.cell.value for tile in known}
    assert 1 in known_values
    assert 2 in known_values


def test_reduce_possible_tiles():
    tiles = [
        Tile((0, 0), Cell(possible_values={1, 2})),
        Tile((0, 1), Cell(possible_values={1, 2})),
        Tile((0, 2), Cell(possible_values={1, 2, 3, 4, 5})),
        Tile((0, 3), Cell(possible_values={3, 4})),
        Tile((0, 4), Cell(possible_values={3, 4})),
    ]
    reduced_tiles = reduce_possible_tiles(tiles)
    final_tiles_by_pos = {tile.position: tile for tile in reduced_tiles}
    assert len(final_tiles_by_pos) == 5
    assert final_tiles_by_pos[(0, 0)].cell.possible_values == {1, 2}
    assert final_tiles_by_pos[(0, 1)].cell.possible_values == {1, 2}
    assert final_tiles_by_pos[(0, 2)].cell.possible_values == {5}
    assert final_tiles_by_pos[(0, 3)].cell.possible_values == {3, 4}
    assert final_tiles_by_pos[(0, 4)].cell.possible_values == {3, 4}


def test_step(simple_puzzle):
    new_puzzle = step(simple_puzzle)
    # Check that some possibilities have been reduced
    assert len(new_puzzle[0, 2].possible_values) < 9