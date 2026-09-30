import numpy as np
import itertools
from typing_extensions import Self

from puzzle import Puzzle


class Solver:
    """
    An abstract solver class for Challenger Puzzles

    :attr puzzle: the Challenger Puzzle object for solving
    """

    def __init__(self: Self, puzzle: Puzzle) -> None:
        """
        Initializes a puzzle solver

        :param puzzle: the puzzle to be solved
        """
        self.puzzle = puzzle

    def solve(self: Self) -> object:
        """
        Solves the given Challenger puzzle

        :return: solution(s)
        """
        NotImplemented


class LinalgSolver(Solver):
    """
    A Challenger Puzzle solver that uses Linear Algebra

    :attr puzzle: the Challenger Puzzle object for solving
    """

    def __init__(self: Self, puzzle: Puzzle) -> None:
        """
        Initializes a puzzle solver
        """
        super().__init__(puzzle)

    def solve(self: Self) -> list[np.ndarray]:
        """
        Solves the given Challenger puzzle using linear algebra

        :return: all solutions
        """
        augment_matrix = self.create_augment_matrix()

        rref_matrix = self.row_reduce(augment_matrix)

        ### rref_matrix is the reduced row echelon form matrix.

        free_vars = []

        for j in range(rref_matrix.shape[1]-1):

            leading = False

            for i in range(rref_matrix.shape[0]):
                if rref_matrix[i,j] != 0:
                    if all(rref_matrix[i,k] == 0 for k in range(j)):
                        leading = True

            if not leading:
                free_vars.append(j)

        vals_to_test = list(itertools.product([i for i in range(1,10)], repeat = len(free_vars)))
        solutions = []

        for test in vals_to_test:
            all_vars = [0 for i in range(rref_matrix.shape[1] - 1)]

            test_vec = np.zeros((rref_matrix.shape[1]))
            for index in range(len(test)):
                test_vec[free_vars[index]] = test[index]

            for row in rref_matrix:

                free_vars_total = row @ test_vec
                try:
                    all_vars[np.where(row == 1)[0][0]] = row[-1] - free_vars_total
                except IndexError:
                    pass

            for i in range(len(free_vars)):
                all_vars[free_vars[i]] = test[i]

            if max(all_vars) <= 9 and min(all_vars) >= 1:
                if all(var == var//1 for var in all_vars):
                    solutions.append(all_vars)

        self.num_free_vars = len(free_vars)
        self.num_solutions = len(solutions)
        self.sol_arrays = []

        for sol in solutions:
          counter = 0
          self.sol_arrays.append(self.puzzle.prob_array.copy())
          for index in range(self.puzzle._n**2):
              i = index // self.puzzle._n
              j = index % self.puzzle._n
              if np.isnan(self.sol_arrays[-1][i,j]):
                  self.sol_arrays[-1][i,j] = sol[counter]
                  counter += 1

        return self.sol_arrays

    def row_reduce(self: Self, matrix: np.ndarray) -> np.ndarray:
        """
        Performs row reduction (RREF) on an augmented matrix using NumPy.

        Args:
            matrix (np.ndarray): A 2D numpy array representing the augmented matrix.

        Returns:
            np.ndarray: The RREF of the matrix.
        """
        A = matrix.astype(float).copy()
        rows, cols = A.shape
        pivot_row = 0

        for col in range(cols):
            if pivot_row >= rows:
                break

            # Find the pivot in current column
            pivot = np.argmax(np.abs(A[pivot_row:rows, col])) + pivot_row
            if A[pivot, col] == 0:
                continue  # Cannot pivot on this column

            # Swap current row with pivot row
            A[[pivot_row, pivot]] = A[[pivot, pivot_row]]

            # Normalize pivot row
            A[pivot_row] = A[pivot_row] / A[pivot_row, col]

            # Eliminate column entries in other rows
            for r in range(rows):
                if r != pivot_row:
                    A[r] -= A[r, col] * A[pivot_row]

            pivot_row += 1

        return A

    def create_augment_matrix(self: Self) -> np.ndarray:
        """
        Takes puzzle object and creates augmented matrix that represents it where
        the first n rows are the row sums, the next n rows are the column sums, and
        the next two rows are the diagonal and counter-diagonal, respectively. The
        columns of the augmented matrix are the missing celles in the puzzle from
        left to right, top to bottom.

        Args:
            self: Puzzle objet

        Returns:
            np.ndarray: The augmented matrix
        """
        n = self.puzzle._n
        augment_matrix = np.zeros((2*n + 2, n**2 - n + 1))
        num_of_vars = 0

        for index in range(n**2):
            i = index // n
            j = index % n
            if np.isnan(self.puzzle.prob_array[i,j]):
                augment_matrix[i,num_of_vars] = 1
                augment_matrix[n+j,num_of_vars] = 1

                if i == j:
                    augment_matrix[2*n, num_of_vars] = 1
                if i + j == n - 1:
                    augment_matrix[2*n + 1, num_of_vars] = 1

                num_of_vars += 1

        # Add the last value for each of the row sums
        for index in range(n):
            row = self.puzzle.prob_array[index]

            # Create a boolean mask to identify non-NaN values
            non_nan_mask = ~np.isnan(row)

            augment_matrix[index, n**2 - n] = self.puzzle.row_sums[index] - row[non_nan_mask].item()

        # Add the last value for each of the column sums
        for index in range(n):
            col = self.puzzle.prob_array[:, index]

            # Create a boolean mask to identify non-NaN values
            non_nan_mask = ~np.isnan(col)

            augment_matrix[index + n, n**2 - n] = self.puzzle.col_sums[index] - col[non_nan_mask].item()

        # Add the last value for each of the diagonal sums
        diag_total = 0
        for index in range(n):
            if not(np.isnan(self.puzzle.prob_array[index,index])):
                diag_total += self.puzzle.prob_array[index,index]
        augment_matrix[2*n, n**2 - n] = self.puzzle.diag_sums[0] - diag_total

        # Add the last value for each of the counter-diagonal sums
        cdiag_total = 0
        for index in range(n):
            if not(np.isnan(self.puzzle.prob_array[index, n - index - 1])):
                cdiag_total += self.puzzle.prob_array[index, n - index - 1]
        augment_matrix[2*n + 1, n**2 - n] = self.puzzle.diag_sums[1] - cdiag_total

        return augment_matrix