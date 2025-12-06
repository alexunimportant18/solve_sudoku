from .cell import Cell
from copy import deepcopy
from .tile import Tile, Tiles


class Puzzle:
    def __init__(self):
        self._cells = [[Cell() for _ in range(9)] for _ in range(9)]

    def print(self):
        for i in range(9):
            # Build the row string with spaces between cells
            row_parts = []
            for j in range(9):
                cell_value = (
                    str(self._cells[i][j].value) if self._cells[i][j].value else "."
                )
                row_parts.append(cell_value)

            # Print horizontal separator before 3rd and 6th rows
            if i % 3 == 0 and i != 0:
                print("  ------+-------+------")

            # Print the row with vertical separators
            print(
                "  "
                + " ".join(row_parts[0:3])
                + " | "
                + " ".join(row_parts[3:6])
                + " | "
                + " ".join(row_parts[6:9])
            )

    def __getitem__(self, index: tuple[int, int]):
        return self._cells[index[0]][index[1]]

    def __setitem__(self, index: tuple[int, int], value: Cell):
        self._cells[index[0]][index[1]] = value

    def __eq__(self, other: "Puzzle"):
        for row in range(9):
            for col in range(9):
                if self._cells[row][col] != other._cells[row][col]:
                    return False
        return True

    def print_unsolved_values(self):
        for row in range(9):
            for col in range(9):
                if not self._cells[row][col].value:
                    print(
                        f"Cell ({row}, {col}) has possible values {self._cells[row][col].possible_values}"
                    )

    def get_unsolved_cells(self) -> Tiles:
        unsolved_cells = []
        for row in range(9):
            for col in range(9):
                if not self._cells[row][col].value:
                    unsolved_cells.append(Tile((row, col), self._cells[row][col]))
        return unsolved_cells

    def update_single_possible_values(self):
        for row in range(9):
            for col in range(9):
                if len(self._cells[row][col].possible_values) == 1:
                    self._cells[row][col].value = next(
                        iter(self._cells[row][col].possible_values)
                    )

    def is_solved(self) -> bool:
        for row in range(9):
            for col in range(9):
                if not self._cells[row][col].value:
                    return False
        return True

    def copy(self):
        return deepcopy(self)
