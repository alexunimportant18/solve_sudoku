from .puzzle import Puzzle
from .cell import Cell

def read_puzzle(filename: str) -> Puzzle:
    puzzle = Puzzle()
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if (len(line) != 9 and i < 9):
                raise ValueError(f"format error in line {i}, content is [{line}]")
            for j, value_str in enumerate(line):
                if value_str != "x" and value_str != ".":
                    puzzle[i, j].set_value(int(value_str))                    
    puzzle.set_as_initial_state()
    return puzzle