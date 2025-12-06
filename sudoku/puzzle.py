from .cell import Cell
from copy import deepcopy

class Puzzle:
    def __init__(self):
        self._cells = [[Cell() for _ in range(9)] for _ in range(9)]
        self._initial_state = None
    def print(self):
        for i in range(9):
            s = "".join([str(self._cells[i][j].value) if self._cells[i][j].value else "x" for j in range(9)])
            print(s)

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
                    print(f"Cell ({row}, {col}) has possible values {self._cells[row][col].possible_values}")

    def update_single_possible_values(self):
        for row in range(9):
            for col in range(9):
                if len(self._cells[row][col].possible_values) == 1:
                    self._cells[row][col].value = next(iter(self._cells[row][col].possible_values))

    def set_as_initial_state(self):
        self._initial_state = deepcopy(self._cells)