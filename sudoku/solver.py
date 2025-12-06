from .puzzle import Puzzle
from .cell import Cell
from typing import TypeAlias, Generator
from collections import namedtuple

Tile = namedtuple('Tile', ['position', 'cell'])
Tiles: TypeAlias = list[Tile]

def generate_sections(puzzle: Puzzle) -> Generator[Tiles, None, None]:
    section_x = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    section_y = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for i in range(9):
        result = []
        row = i // 3
        col = i - row * 3
        for r in section_x[row]:
            for c in section_y[col]:
                result.append(Tile((r, c), puzzle[r, c]))
        yield result

def generate_rows(puzzle: Puzzle) -> Generator[Tiles, None, None]:
    for r in range(9):
        result = []
        for c in range(9):
            result.append(Tile((r, c), puzzle[r, c]))
        yield result

def generate_cols(puzzle: Puzzle) -> Generator[Tiles, None, None]:
    for c in range(9):
        result = []
        for r in range(9):
            result.append(Tile((r, c), puzzle[r, c]))
        yield result




def extract_cyclic_tiles(tiles: Tiles) -> tuple[Tiles, Tiles, Tiles]:
    """
    Extracts known, cyclic, and remaining tiles from a list of tiles.

    This function first separates tiles that have a known value.
    Then, it sorts the remaining (unknown) tiles based on the number of possible values in their cells.
    It then iterates through the sorted tiles, accumulating the union of possible values.
    If the size of the union equals the number of tiles processed, that group of tiles
    is considered "cyclic". The possible values of the cyclic group are removed from the
    possible values of the remaining tiles.

    Args:
        tiles: A list of tiles.

    Returns:
        A tuple containing three lists of tiles:
        - The first list contains the known tiles.
        - The second list contains the cyclic tiles found.
        - The third list contains the remaining tiles with updated possible values.
        If no cyclic group is found, the second list is empty.
    """
    # Filter out tiles that already have a value.
    unknown_tiles = [tile for tile in tiles if tile.cell.value is None]
    known_tiles = [tile for tile in tiles if tile.cell.value is not None]

    known_values = [tile.cell.value for tile in known_tiles]
    for tile in unknown_tiles:
        tile.cell.possible_values -= set(known_values)

    # Sort unknown tiles by the length of possible_values
    sorted_tiles = sorted(unknown_tiles, key=lambda tile: len(tile.cell.possible_values))

    for i in range(2, len(sorted_tiles) + 1):
        from itertools import combinations
        for group in combinations(sorted_tiles, i):
            union = set()
            for tile in group:
                union.update(tile.cell.possible_values)
            
            if len(union) == i:
                cyclic_tiles = list(group)
                remaining_tiles_raw = [tile for tile in sorted_tiles if tile not in cyclic_tiles]
                
                remaining_tiles = []
                for t in remaining_tiles_raw:
                    new_possible_values = t.cell.possible_values - union
                    if len(new_possible_values) == 1:
                        new_cell = Cell(value=next(iter(new_possible_values)), possible_values=new_possible_values)
                        known_tiles.append(Tile(position=t.position, cell=new_cell))
                    else:
                        new_cell = Cell(value=t.cell.value, possible_values=new_possible_values)
                        remaining_tiles.append(Tile(position=t.position, cell=new_cell))

                return known_tiles, cyclic_tiles, remaining_tiles

    # No cyclic group found, so all unknown tiles are considered "remaining"
    return known_tiles, [], unknown_tiles


def reduce_possible_tiles(tiles: Tiles) -> Tiles:
    """
    Deducts possible values from tiles based on the values of other tiles in the same row, column, or section.

    Args:
        tiles: A list of tiles.

    Returns:
        A list of tiles with updated possible values.
    """
    result = []
    processing_tiles = tiles
    while True:
        known_tiles, cyclic_tiles, remaining_tiles = extract_cyclic_tiles(processing_tiles)
        result.extend(known_tiles)
        result.extend(cyclic_tiles)
        if not cyclic_tiles:
            result.extend(remaining_tiles)
            break
        processing_tiles = remaining_tiles

    return result


def step(puzzle: Puzzle) -> Puzzle:
    result = Puzzle()
    for section in generate_sections(puzzle):
        output = reduce_possible_tiles(section)
        for tile in output:
            result[tile.position] = tile.cell

    for row in generate_rows(result):
        output = reduce_possible_tiles(row)
        for tile in output:
            result[tile.position] = tile.cell

    result.print()
    for col in generate_cols(result):
        output = reduce_possible_tiles(col)
        for tile in output:
            result[tile.position] = tile.cell

    result.update_single_possible_values()
    print("-" * 20)
    result.print()
    print("-" * 20)
    return result