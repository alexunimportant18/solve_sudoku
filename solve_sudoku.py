import typer
from typing_extensions import Annotated
from sudoku.puzzle_file import read_puzzle
import sudoku.solver
from sudoku.solver import step, generate_sections

app = typer.Typer()

@app.command()
def main(puzzle_file: Annotated[str, typer.Argument(metavar="puzzle_file", help="The path to the file containing the Sudoku puzzle.")]):   
    """
    Solve a Sudoku puzzle. The definition of the puzzle in in the given text file.

        The puzzle file should contain 9 lines, each line with 9 characters.
        Each character is either a digit from 1 to 9 or a dot (.) to represent an empty cell.
    """
    puzzle = read_puzzle(puzzle_file)
    puzzle.print()

    print("-" * 20)
    
    while True:
        new_puzzle = step(puzzle)
        if new_puzzle == puzzle:
            break
        puzzle = new_puzzle

    print("-" * 20)
    puzzle.print()
    puzzle.print_unsolved_values()
    puzzle.update_single_possible_values()
    puzzle.print_unsolved_values()
    


if __name__ == "__main__":
    app()