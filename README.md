# The Challenger Puzzle

## Background
The Challenger puzzle is a newspaper puzzle where the goal is to fill empty cells with integer values 1 through 9 such that the rows, columns, main diagonal, and main counter-diagonal all sum to the corresponding values along the border. Each Challenger puzzle provides four filled-in values, one per row and columnn. 

<p align="center">
  <img src="assets/example.png" alt="Challenger Puzzle" width="600">
</p>

One difference between the Challenger puzzle and many other newspaper puzzles is that the Challenger puzzle is not required to be well-posed, meaning that it may have more than one valid solution. This code accompanies a forthcoming paper that establishes necessary and sufficient conditions for well-posedness and determines that exactly 754,932,143,813,544 well-posed Challenger puzzles exist. 

## Code Usage
### Generating Challenger Puzzles
To print a random Challenger puzzle, run `generator.py`:

```bash
python generator.py
```

To generate a puzzle within code, run

```python
from generator import Generator

my_puzzle = Generator().generate()
```

### Solving Challenger Puzzles
To solve a Challenger puzzle, either generate a random one or create a `Puzzle` object by defining `prob_array`, `row_sums`, `col_sums`, and `diag_sums`. Then

```python
from solver import LinAlgSolver

sol = LinalgSolver(my_puzzle).solve() # get all solutions
print("Number of solutions:", len(sol)) # count solutions
print("First solution:\n", sol[0]) # see a particular solution
```