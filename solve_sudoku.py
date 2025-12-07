import typer
from typing_extensions import Annotated
from sudoku.puzzle_file import read_puzzle
from sudoku.solver import try_solve_puzzle, SolverResult
from rich import print

app = typer.Typer()


@app.command()
def main(
    puzzle_file: Annotated[
        str,
        typer.Argument(
            metavar="puzzle_file",
            help="The path to the file containing the Sudoku puzzle.",
        ),
    ],
):
    """
    Solve a Sudoku puzzle. The definition of the puzzle in in the given text file.

        The puzzle file should contain 9 lines, each line with 9 characters.
        Each character is either a digit from 1 to 9 or a dot (.) to represent an empty cell.
    """
    puzzle = read_puzzle(puzzle_file)
    print("[green]Input Puzzle:[/green]\n")
    puzzle.print()

    solved, puzzle, iteration = try_solve_puzzle(puzzle)

    while solved == SolverResult.UNSOLVED:
        print(
            "\nPuzzle is not solved by just removing cyclic cells, need to do trial-and-error"
        )
        # puzzle is not solved yet, pick one cell and assign a possible value and try to solve again
        unsolved_cells = puzzle.get_unsolved_cells()
        if unsolved_cells:
            unsolved_cells.sort(key=lambda tile: len(tile.cell.possible_values))

            try_cell = unsolved_cells[0]
            original_puzzle = puzzle.copy()
            for possible_value in iter(try_cell.cell.possible_values):
                puzzle = original_puzzle.copy()
                print(
                    f"Try to assign value {possible_value} to cell ({try_cell.position})"
                )
                try_cell.cell.set_value(possible_value, {possible_value})
                row, col = try_cell.position
                puzzle[row, col] = try_cell.cell

                solved, puzzle, iteration = try_solve_puzzle(puzzle, iteration + 1)
                if solved == SolverResult.SOLVED or solved == SolverResult.UNSOLVED:
                    break
                else:
                    print(
                        f"\nValue {possible_value} is not valid for cell ({try_cell.position}), try next value"
                    )

            # consumed all of the possible values
            if solved == SolverResult.SOLVED:
                break
            if solved == SolverResult.FAILURE:
                print(
                    f"\nFailed to solve the puzzle after trying all possible values for cell ({try_cell.position})"
                )
                break
            if solved == SolverResult.UNSOLVED:
                print(f"\nPuzzle is not solved yet, try to fill in value of another cell")
                continue

        

    # print the result
    print()
    print("[green]Solved Puzzle:[/green]\n")
    puzzle.print()
    # puzzle.print_unsolved_values()
    # puzzle.update_single_possible_values()
    # puzzle.print_unsolved_values()


if __name__ == "__main__":
    app()
