# Sudoku Solver

A Python-based Sudoku puzzle solver that uses constraint propagation and elimination techniques to solve 9x9 Sudoku puzzles.

## Features

- **Constraint Propagation**: Uses advanced logic to eliminate impossible values from cells
- **Cyclic Group Detection**: Identifies groups of cells that must contain specific values
- **Interactive CLI**: Command-line interface with rich formatting for clear puzzle display
- **Comprehensive Testing**: Full test suite with pytest for reliability
- **Modern Python**: Built with Python 3.11+ using modern type hints and best practices

## Installation

This project uses [uv](https://docs.astral.sh/uv/) as the project manager.

```bash
# Clone the repository
git clone <repository-url>
cd sudoku

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

## Usage

### Solving a Sudoku Puzzle

```bash
# Using uv run (recommended)
uv run solve_sudoku.py puzzle.txt

# Or after activating the virtual environment
python solve_sudoku.py puzzle.txt
```

### Puzzle File Format

The puzzle file should contain 9 lines, each with 9 characters:

- Use digits 1-9 for filled cells
- Use dots (.) or 'x' for empty cells

Example puzzle file (`puzzle.txt`):

```bash
x7xxxx6xx
xx8xxxx41
9xx8xxxxx
xxxxxxxx4
3xx1x7xx2
79xxx63xx
5xxxxx9xx
x6x2x9xxx
xxx5x3xxx
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=sudoku --cov-report=html

# Run specific test file
uv run pytest tests/test_solver.py
```

## Project Structure

```bash
sudoku/
├── sudoku/ # Core package
│ ├── init.py
│ ├── cell.py # Cell class representing individual Sudoku cells
│ ├── puzzle.py # Puzzle class managing the 9x9 grid
│ ├── puzzle_file.py # File I/O for reading puzzle files
│ └── solver.py # Solving algorithms and constraint propagation
├── tests/ # Test suite
│ ├── test_cell.py
│ ├── test_puzzle.py
│ └── test_solver.py
├── solve_sudoku.py # Main CLI application
├── pyproject.toml # Project configuration
└── README.md # This file
```

## Algorithm

The solver uses a sophisticated constraint propagation approach:

1. **Section Analysis**: Divides the puzzle into 3x3 sections, rows, and columns
2. **Known Value Elimination**: Removes impossible values based on known digits
3. **Cyclic Group Detection**: Identifies groups of N cells that must contain N specific values
4. **Iterative Refinement**: Repeatedly applies constraints until no further progress can be made

This approach can solve many Sudoku puzzles without resorting to brute-force backtracking.

## Development

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name
```

### Code Quality

The project follows modern Python best practices:

- Type hints throughout the codebase
- Comprehensive docstrings
- Unit tests with good coverage
- Clean, modular architecture

## Examples

### Basic Usage

```bash
# Solve a puzzle
uv run solve_sudoku.py puzzle.txt

# Output:
# Input Puzzle:
#
# . 7 . | . . . | 6 . .
# . . 8 | . . . | . 4 1
# 9 . . | 8 . . | . . .
# ------+-------+------
# . . . | . . . | . . 4
# 3 . . | 1 . 7 | . . 2
# 7 9 . | . . 6 | 3 . .
# ------+-------+------
# 5 . . | . . . | 9 . .
# . 6 . | 2 . 9 | . . .
# . . . | 5 . 3 | . . .
#
# --------------------
#
# Solved Puzzle:
#
# [Solved grid will be displayed here]
```

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
